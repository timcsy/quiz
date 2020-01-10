export const state = () => ({
	id: '',
	imageScore: '',
	imageCorr: '',
	imageAnalysis: {},
	analysis: {},
	score: '',
	consistency: '',
	corr: {},
	questions: [],
	selections: [],
	splitMethod: 'odd',
	splitResult: '',
	waitAnalysis: false,
	waitCorr: false,
	waitSplit: false
})

export const mutations = {
	images (state, images) {
		state.imageScore = images.score
		state.imageCorr = images.corr
		state.imageAnalysis = images.analysis
	}
}
