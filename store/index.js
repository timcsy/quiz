import { getField, updateField } from 'vuex-map-fields'

export const state = () => ({
	title: 'Quiz',
	drawer: [
		{
			icon: 'mdi-home',
			title: '首頁',
			to: '/'
		},
		{
			icon: 'mdi-pencil',
			title: '評量',
			to: '/test'
		}
	],
	action: null,
	questions: {},
	responses: {}
})

export const getters = {
	// Add the `getField` getter to the
	// `getters` of your Vuex store instance.
	getField
}

export const mutations = {
	updateField
}
