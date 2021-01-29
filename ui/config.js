import {publicPath} from "./vue.config"
const config = {
    api: process.env.NODE_ENV == 'production' ? `${publicPath}api/` : 'http://127.0.0.1:5000/api',
    imgur_client_id: "e41ec52ccc51322"
}
export { config }
export default {  }