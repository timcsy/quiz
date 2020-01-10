<template>
	<v-container>
		<v-container v-if="waitAnalysis">
			<v-row align="center" justify="center">
				<v-progress-circular
					:size="72"
					indeterminate
				/>
			</v-row>
			<v-row align="center" justify="center" class="ma-8">
				處理中，請稍候
			</v-row>
		</v-container>
		<v-container v-else>
			<v-row class="display-1 font-weight-medium">
				<v-col>測驗分析</v-col>
			</v-row>
			<v-row>
				<v-col cols="12">
					<data-frame :data="analysis" simple />
				</v-col>
			</v-row>
			<v-row justify="start">
				<v-col
					v-for="(url, key) in imageAnalysis"
					:key="key"
					xs="12"
					sm="8"
					md="6"
					xl="4"
				>
					<v-img :src="url" />
				</v-col>
			</v-row>
			<v-row class="display-1 font-weight-medium">
				<v-col>分數分佈</v-col>
			</v-row>
			<v-row align="center" justify="center">
				<v-col
					xs="12"
					sm="8"
					md="6"
					xl="4"
				>
					<v-img :src="imageScore" />
				</v-col>
				<v-col v-html="score" />
			</v-row>
			<v-row class="display-1 font-weight-medium">
				<v-col>內部一致性</v-col>
			</v-row>
			<v-row>
				<v-col v-html="consistency" />
			</v-row>
			<v-row v-if="!waitCorr">
				<v-col>
					<v-btn
						@click="showCorr()"
					>
						顯示兩兩關係圖（較耗時）
					</v-btn>
				</v-col>
			</v-row>
			<v-container v-if="waitCorr">
				<v-row justify="center">
					<v-progress-circular
						:size="48"
						indeterminate
					/>
				</v-row>
				<v-row justify="center" class="ma-8">
					處理中，請稍候
				</v-row>
			</v-container>
			<v-row v-else>
				<v-img :src="imageCorr" />
			</v-row>
			<v-row>
				<v-col cols="12">
					<data-frame :data="corr" :selected.sync="selections" show-select />
				</v-col>
			</v-row>
			<v-row>
				<v-col>折半信度：</v-col>
			</v-row>
			<v-row>
				<v-col
					xs="12"
					sm="6"
					md="4"
					lg="3"
					xl="2"
				>
					<v-select
						:items="splitChoices"
						v-model="splitMethod"
						label="選擇拆半方法"
					/>
				</v-col>
			</v-row>
			<v-row v-if="!waitSplit">
				<v-col>
					<v-btn
						@click="calculateSplit()"
					>
						計算折半信度
					</v-btn>
				</v-col>
			</v-row>
			<v-container v-if="waitSplit">
				<v-row justify="center">
					<v-progress-circular
						:size="48"
						indeterminate
					/>
				</v-row>
				<v-row justify="center" class="ma-8">
					處理中，請稍候
				</v-row>
			</v-container>
			<v-row v-else>
				<v-col v-html="splitResult" />
			</v-row>
		</v-container>
	</v-container>
</template>

<script>
import axios from 'axios'
import { mapFields } from 'vuex-map-fields'
import DataFrame from '~/components/DataFrame.vue'

export default {
  layout: 'default',
	components: {
		DataFrame
	},
	props: {
	},
	data () {
		return {
			splitChoices: [
				{ 'text': '自訂', 'value': 'custom' },
				{ 'text': '奇偶拆', 'value': 'odd' },
				{ 'text': '前後拆', 'value': 'front' }
			]
		}
	},
	computed: {
		...mapFields([
      'analysis.id',
			'analysis.imageScore',
			'analysis.imageCorr',
			'analysis.imageAnalysis',
			'analysis.analysis',
			'analysis.score',
			'analysis.consistency',
			'analysis.corr',
			'analysis.questions',
			'analysis.selections',
			'analysis.splitMethod',
			'analysis.splitResult',
			'analysis.waitAnalysis',
			'analysis.waitCorr',
			'analysis.waitSplit'
		]),
		...mapFields({
			title: 'title',
			action: 'action',
			test: 'test'
		})
	},
	watch: {
		splitMethod () {
			this.splitChoiceChange()
		},
		questions () {
			this.splitChoiceChange()
		}
	},
	created () {
	},
	async mounted () {
		this.title = '測驗分析'
		if (this.action === null) {
			this.waitAnalysis = true
			const data = (await axios.post('/api/analysis', {
				id: this.id,
				test: {
					questions: this.test.questions,
					responses: this.test.responses
				}
			})).data
			this.imageAnalysis = data.images.analysis
			this.imageScore = data.images.score
			this.analysis = data.analysis
			this.score = data.score.replace(/\r\n/g, '<br>')
			this.consistency = data.consistency.replace(/\r\n/g, '<br>')
			this.corr = data.corr
			this.questions = Object.values(data.test.questions).map(q => q.name)
			this.splitResult = ''
			this.splitChoiceChange()
		}
		this.action = 'test'
		this.waitAnalysis = false
	},
	methods: {
		async showCorr () {
			this.waitCorr = true
			try {
				const data = (await axios.post('/api/corr', { id: this.id, columns: this.selections })).data
				this.imageCorr = data.images.corr
			} catch (err) {
			}
			this.waitCorr = false
		},
		splitChoiceChange () {
			if (this.splitMethod === 'odd') {
				this.selections = this.questions.filter((q, i) => i % 2 === 0)
				this.splitMethod = 'custom'
			} else if (this.splitMethod === 'front') {
				this.selections = this.questions.slice(0, Math.ceil(this.questions.length / 2))
				this.splitMethod = 'custom'
			}
		},
		async calculateSplit () {
			const first = this.selections
			const second = this.questions.filter(q => !first.includes(q))
			this.waitSplit = true
			const data = (await axios.post('/api/split', { id: this.id, first, second })).data
			this.splitResult = data.splitResult.replace(/\r\n/g, '<br>')
			this.waitSplit = false
		}
	}
}
</script>

<style>

</style>
