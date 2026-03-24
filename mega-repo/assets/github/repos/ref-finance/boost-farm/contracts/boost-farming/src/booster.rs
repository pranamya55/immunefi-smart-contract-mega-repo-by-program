use std::cmp::Ordering;

use crate::*;

#[derive(BorshSerialize, BorshDeserialize, Serialize, Deserialize)]
#[serde(crate = "near_sdk::serde")]
pub struct BoosterInfo {
    pub booster_decimal: u32,
    /// <affected_seed_id, log_base>
    pub affected_seeds: HashMap<SeedId, U128>,
    #[serde(with = "u128_dec_format")]
    pub boost_suppress_factor: u128,
}

impl BoosterInfo {
    pub fn assert_valid(&self, booster_id: &SeedId) {
        require!(self.affected_seeds.contains_key(booster_id) == false, E202_FORBID_SELF_BOOST);
        require!(self.affected_seeds.len() <= MAX_NUM_SEEDS_PER_BOOSTER, E204_EXCEED_SEED_NUM_IN_BOOSTER);
        require!(self.boost_suppress_factor > 0, E206_INVALID_BOOST_SUPPRESS_FACTOR);
    }
}

#[near_bindgen]
impl Contract {
    #[payable]
    pub fn modify_booster(&mut self, booster_id: SeedId, booster_info: BoosterInfo) {
        assert_one_yocto();
        require!(self.is_owner_or_operators(), E002_NOT_ALLOWED);
        require!(self.data().state == RunningState::Running, E004_CONTRACT_PAUSED);
        require!(self.internal_get_seed(&booster_id).is_some(), E301_SEED_NOT_EXIST);
        booster_info.assert_valid(&booster_id);

        let mut config =  self.data().config.get().unwrap();
        require!(config.booster_seeds.keys().all(|booster_seed_id| !booster_info.affected_seeds.contains_key(booster_seed_id)), E207_FORBID_BOOST_BOOSTER_SEED);
        for (_, exist_booster_info) in &config.booster_seeds {
            require!(!exist_booster_info.affected_seeds.contains_key(&booster_id), E207_FORBID_BOOST_BOOSTER_SEED);
        }
        require!(self.affected_farm_count(&booster_info) <= config.max_num_farms_per_booster, E203_EXCEED_FARM_NUM_IN_BOOST);
        
        config.booster_seeds.insert(booster_id.clone(), booster_info);
        self.data_mut().config.set(&config);
    }
}

impl Contract {

    fn affected_farm_count(&self, booster_info: &BoosterInfo) -> u32 {
        booster_info.affected_seeds
        .keys()
        .map(|seed_id| self.data().seeds.get(seed_id).expect(E301_SEED_NOT_EXIST))
        .map(|v| {
            let seed: Seed = v.into();
            seed.farms.len() as u32
        })
        .sum::<u32>()
    }

    pub fn assert_booster_affected_farm_num(&self) {
        let config = self.internal_config();
        for booster_info in config.booster_seeds.values() {
            require!(self.affected_farm_count(booster_info) <= config.max_num_farms_per_booster, E203_EXCEED_FARM_NUM_IN_BOOST);
        }
    }

    /// generate booster ratios map for a given seed
    pub fn gen_booster_ratios(&self, seed_id: &SeedId, farmer: &Farmer) -> HashMap<SeedId, f64> {
        let mut ratios = HashMap::new();
        let boosters = self.internal_config().get_boosters_from_seed(seed_id);
        for (booster, booster_decimal, booster_log_base, boost_suppress_factor) in &boosters {
            let booster_base = 10u128.pow(*booster_decimal) * boost_suppress_factor;
            let booster_balance = farmer
                .get_seed(booster)
                .map(|v| v.x_locked_amount)
                .unwrap_or(0_u128);
            if booster_balance > booster_base {
                let log_base = (*booster_log_base as f64) / 10f64.powi(*booster_decimal as i32);
                let booster_amount = booster_balance as f64 / booster_base as f64;
                let ratio = booster_amount.log(log_base);
                ratios.insert(booster.clone(), ratio);
            }
        }
        ratios
    }

    /// if seed_id is a booster, then update all impacted seed
    pub fn update_impacted_seeds(&mut self, farmer: &mut Farmer, booster_id: &SeedId) {
        if let Some(booster_info) = self.internal_config().get_affected_seeds_from_booster(booster_id) {
            for seed_id in booster_info.affected_seeds.keys() {
                // here we got each affected seed_id, then if the farmer has those seeds, should be updated on by one
                if farmer.get_seed(seed_id).is_some() {
                    // first claim that farmer's current reward and update boost_ratios for the seed
                    self.internal_do_farmer_claim(farmer, &seed_id);
                }
            }
        }
    }

    pub fn sync_booster_policy(&mut self, farmer: &mut Farmer) {
        let config = self.internal_config();
        for booster_seed_id in config.booster_seeds.keys() {
            if farmer.get_seed(booster_seed_id).is_some() {
                self.internal_do_farmer_claim(farmer, booster_seed_id);
                
                let mut farmer_seed = farmer.get_seed_unwrap(booster_seed_id);
                let mut booster_seed = self.internal_unwrap_seed(booster_seed_id);

                if farmer_seed.unlock_timestamp > env::block_timestamp() {
                    let prev = farmer_seed.get_seed_power();
                    farmer_seed.sync_locking_policy(&config, booster_seed.min_locking_duration_sec);
                    let next = farmer_seed.get_seed_power();
                    farmer.set_seed(booster_seed_id, farmer_seed);

                    let need_update = match prev.cmp(&next) {
                        Ordering::Greater => {
                            booster_seed.total_seed_power -= prev - next;
                            true
                        }
                        Ordering::Less => {
                            booster_seed.total_seed_power += next - prev;
                            true
                        }
                        Ordering::Equal => { false }
                    };
                    
                    if need_update {
                        self.internal_set_seed(booster_seed_id, booster_seed);
                        self.update_impacted_seeds(farmer, &booster_seed_id);
                    }
                } else {
                    let (unlock_amount, decreased_seed_power) = farmer_seed.try_unlock_all_to_free();
                    if unlock_amount > 0 {
                        farmer.set_seed(booster_seed_id, farmer_seed);

                        booster_seed.total_seed_power -= decreased_seed_power;

                        self.internal_set_seed(booster_seed_id, booster_seed);

                        self.update_impacted_seeds(farmer, &booster_seed_id);

                        Event::SeedUnlock {
                            farmer_id: &farmer.farmer_id,
                            seed_id: &booster_seed_id,
                            unlock_amount: &U128(unlock_amount),
                            decreased_power: &U128(decreased_seed_power),
                            slashed_seed: &U128(0),
                        }
                        .emit();
                    }
                }
            }
        }
    }

}