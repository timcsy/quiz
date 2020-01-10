<template>
  <v-container>
    <!-- You can change <v-container> to other root component -->
  </v-container>
</template>

<script>
import { mapFields } from 'vuex-map-fields'
// import OtherComponent from '~/components/OtherComponent.vue'

export default {
  layout: 'default',
	components: {
	},
	props: {
	},
	head () {
		return {
			title: '首頁'
		}
	},
	data () {
		return {
		}
	},
	computed: {
		...mapFields({
			title: 'title'
		})
	},
	watch: {
	},
	created () {
	},
	mounted () {
		this.title = 'Quiz'
	},
	methods: {
	}
}
</script>

<style>

</style>
