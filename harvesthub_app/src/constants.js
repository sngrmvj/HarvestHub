const BASE_URL = "http://localhost:5004";
const LOGINURL = `${BASE_URL}/retailer/login`;
const SIGNUPURL = `${BASE_URL}/retailer/register`;
const GET_COMMODITIES = `${BASE_URL}/retailer/commodties`;
const DELETE_ITEM_IN_CART = `${BASE_URL}/retailer/cart`;
const ADD_TO_CART = `${BASE_URL}/retailer/cart`;
const ALL_ORDERS = `${BASE_URL}/retailer/receipts`


export {
    LOGINURL,
    SIGNUPURL,
    GET_COMMODITIES,
    ADD_TO_CART,
    DELETE_ITEM_IN_CART,
    ALL_ORDERS
}