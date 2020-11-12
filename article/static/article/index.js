var dataDict = {'category': '', 'score': ''};

Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            articleList: null,
        }
    },
    mounted(){
        axios
            .get('/api/article-list')
            .then(response => {
                this.articleList = response.data;
            })
            .catch(function (error) {
                console.log(error);
            });
    },
    methods: {
        onChange(event) {
            dataDict[event.target.name] = event.target.value;
            console.log(dataDict)
        },
        fetchApi() {
            axios
                .get(`/api/article-list?category=${dataDict.category}&score=${dataDict.score}`)
                .then(response => {
                    this.articleList = response.data;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
    }
}).mount('#article')