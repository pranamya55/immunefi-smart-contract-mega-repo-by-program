use near_sdk::borsh::{self, BorshDeserialize, BorshSerialize};
use near_sdk::json_types::U128;
use near_sdk::{near_bindgen, AccountId, PanicOnDefault};

#[near_bindgen]
#[derive(BorshDeserialize, BorshSerialize, PanicOnDefault)]
pub struct Contract;

#[near_bindgen]
impl Contract {
    #[init]
    pub fn new() -> Self {
        Self
    }

    #[allow(unused_variables)]
    pub fn on_cast_shadow(
        &mut self,
        account_id: AccountId,
        shadow_id: String,
        amount: U128,
        msg: String,
    ) {
    }

    #[allow(unused_variables)]
    pub fn on_remove_shadow(
        &mut self,
        account_id: AccountId,
        shadow_id: String,
        amount: U128,
        msg: String,
    ) {
    }
}
