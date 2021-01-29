const config = {
    api: process.env.NODE_ENV === 'production' ? '/api' : 'http://127.0.0.1:5000/api',
    imgur_client_id: "e41ec52ccc51322"
}
export default { config }