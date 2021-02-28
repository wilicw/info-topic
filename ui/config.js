import { publicPath } from "./vue.config"
const config = {
    title: "大安資訊專題網",
    api: process.env.NODE_ENV == 'production' ? `${publicPath}api` : 'http://127.0.0.1:5000/api'
}
export { config }
export default {}