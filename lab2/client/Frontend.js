import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.6.12/dist/vue.esm.browser.js'

Vue.component('loader', {
    template: `
    <div style="display: flex;justify-content: center;align-items: center">
      <div class="spinner-border" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    </div>
  `
})

new Vue(
    {
        el: '#app',
        data() {
            return{
                loading: false,
                form: {
                    date_input_start: '',
                    date_input_end: '',
                    city: ''
                },
                dates: [],
                cards: []

            }
        },
       computed: {
            canCreate(){
                return this.form.date_input_start.trim()&&this.form.date_input_end.trim()&&this.form.city
            }
        },

        methods: {
            async createDate(){
                const {...date} = this.form //
                this.dates = {...date}


                this.cards = await request('/api/conect', 'POST', date)
                console.log(this.cards)

            }
        },
        async mounted(){
            this.loading = true
            this.dates = await request('/api/conect', 'GET')
            this.loading = false

        }
        // сделать запрос с фронтэнда
    })
async function request(url, method = 'GET', data = null) {
    try{
        const headers = {}
        let body
        let param
        if (data){
            headers['Content-Type']= 'application/json'
            body = JSON.stringify(data)
        }
        const response = await fetch(url, {
            method,
            headers,
            body,

        })
        if (method )
            return await response.json()
    } catch(e) {
        console.warn('Error', e.message)
    }
}




