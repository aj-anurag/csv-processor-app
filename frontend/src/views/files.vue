<template>
    <ag-grid-vue style="width: 500px; height: 200px" class="ag-theme-alpine" :columnDefs="columnDefs"
        :rowData="rowData">
    </ag-grid-vue>
</template>

<script>
import { AgGridVue } from "ag-grid-vue3";  // the AG Grid Vue Component
import "ag-grid-community/styles/ag-grid.css"; // Core grid CSS, always needed
import "ag-grid-community/styles/ag-theme-alpine.css"; // Optional theme CSS

export async function call(urlToUser) {
    return await fetch(urlToUser)
        .then(response => {
            return response.text()
        })
        .then((data) => {
            return (data ? JSON.parse(data) : {})
        })
        .catch((error) => {
            reject(error)
        })

}

export default {
    name: "App",
    data() {
        return {
            columnDefs: null,
            rowData: null
        };
    },

    components: {
        AgGridVue
    },
    beforeMount() {
        this.columnDefs = [

        ];

        this.rowData = [

        ];
        call('http://127.0.0.1:8000/main')
            .then(rowData => { 
                const keys = Object.keys(rowData[0])
                keys.forEach(key => this.columnDefs.push({ field: key, sortable: true, filter: true }));
                this.rowData = rowData 
            });
    },

};
</script>

<style lang="scss">


</style>