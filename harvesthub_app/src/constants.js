const BASE_URL = "http://localhost:5004";
const LOGINURL = `${BASE_URL}/retailer/login`;
const SIGNUPURL = `${BASE_URL}/retailer/register`;
const GET_COMMODITIES = `${BASE_URL}/retailer/commodties`;
const GET_CART = `${BASE_URL}/retailer/cart`
const DELETE_ITEM_IN_CART = `${BASE_URL}/retailer/cart`;
const ADD_TO_CART = `${BASE_URL}/retailer/cart`;
const ALL_ORDERS = `${BASE_URL}/retailer/receipts`;
const GET_RECEIPT = `${BASE_URL}/retailer/receipt`;
const PURCHASE_ORDER = `${BASE_URL}/retailer/purchase`;
const VALIDATE_USER = `${BASE_URL}/retailer/validate`;


export {
    LOGINURL,
    SIGNUPURL,
    GET_COMMODITIES,
    GET_CART,
    ADD_TO_CART,
    DELETE_ITEM_IN_CART,
    ALL_ORDERS,
    GET_RECEIPT,
    PURCHASE_ORDER,
    VALIDATE_USER
}