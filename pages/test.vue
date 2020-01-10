<template>
  <v-container>
		<v-row>
			<v-col>
				<v-file-input v-model="files.questions" accept="*/*" label="測驗（請選擇檔案）" />
				<v-file-input v-model="files.responses" accept="*/*" label="回應（請選擇檔案）" />
				<v-row justify="center">
					<v-btn
						@click="upload()"
					>
						上傳檔案
					</v-btn>
				</v-row>
			</v-col>
		</v-row>
		<v-container v-if="state === 'uploading'">
			<v-row align="center" justify="center">
				<v-progress-circular
					:size="72"
					indeterminate
				/>
			</v-row>
			<v-row align="center" justify="center" class="ma-8">
				上傳中，請稍候
			</v-row>
		</v-container>
		<v-container v-if="state === 'finished'">
			<v-row class="display-1 font-weight-medium">
				<v-col>欄位對應</v-col>
			</v-row>
			<v-row>
				<v-col xs="12" sm="6" md="4" lg="3" xl="2">
					<v-select :items="columns" v-model="name" label="題號" />
				</v-col>
				<v-col xs="12" sm="6" md="4" lg="3" xl="2">
					<v-select :items="columns" v-model="score" label="配分" />
				</v-col>
			</v-row>
			<v-row>
				<v-col xs="12" sm="6" md="4" lg="3" xl="2">
					<v-select :items="columns" v-model="text" label="題目" />
				</v-col>
				<v-col xs="12" sm="6" md="4" lg="3" xl="2">
					<v-select :items="columns" v-model="answer" label="答案" />
				</v-col>
			</v-row>
			<v-row>
				<v-col xs="12" sm="6" md="4" lg="3" xl="2">
					<v-select :items="columns" v-model="type" label="類別" />
				</v-col>
				<v-col xs="12" sm="6" md="4" lg="3" xl="2">
					<v-select :items="types" v-model="boolean" label="類別文字（是非）" />
				</v-col>
			</v-row>
			<v-row>
				<v-col xs="12" sm="6" md="4" lg="3" xl="2">
					<v-select :items="types" v-model="discrete" label="類別文字（單選）" />
				</v-col>
				<v-col xs="12" sm="6" md="4" lg="3" xl="2">
					<v-select :items="types" v-model="continuous" label="類別文字（連續計分）" />
				</v-col>
			</v-row>
			<v-row class="display-1 font-weight-medium">
				<v-col>測驗</v-col>
			</v-row>
			<v-row>
				<v-col cols="12">
					<data-frame :data="questions" :selected.sync="selected.questions" show-select />
				</v-col>
			</v-row>
			<v-row class="display-1 font-weight-medium">
				<v-col>回應</v-col>
			</v-row>
			<v-row>
				<v-col cols="12">
					<data-frame :data="responses" :selected.sync="selected.rows" show-select />
				</v-col>
			</v-row>
			<v-row>
				<v-col>
					<v-row justify="center">
						<v-btn
							@click="analysis()"
						>
							測驗分析
						</v-btn>
					</v-row>
				</v-col>
			</v-row>
		</v-container>
  </v-container>
</template>

<script>
import axios from 'axios'
import { mapFields } from 'vuex-map-fields'
import { loc, getRow, getCol } from '~/plugins/utils'
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
			modified: false,
			files: {
				question: null,
				responses: null
			},
			selected: {
				questions: [],
				rows: []
			}
		}
	},
	computed: {
		...mapFields([
      'questions',
			'responses',
			'test.state',
			'test.name',
			'test.score',
			'test.text',
			'test.answer',
			'test.type',
			'test.boolean',
			'test.discrete',
			'test.continuous',
			'test.selectedQuestions',
			'test.selectedRows'
		]),
		...mapFields({
			title: 'title',
			action: 'action',
			id: 'analysis.id',
			testQuestions: 'test.questions',
			testResponses: 'test.responses'
		}),
		columns () {
			if (Object.keys(this.questions).length > 0) {
				return Object.keys(Object.values(this.questions)[0]).map(c => (c === null) ? 'nan' : c)
			} else {
				return []
			}
		},
		types () {
			return [...new Set(Object.values(getCol(this.questions, true, this.type)))]
		}
	},
	watch: {
		'selected.questions' () {
			this.modified = true
			this.linkQuestions()
		},
		'selected.rows' () {
			this.modified = true
			this.selectedRows = this.selected.rows
		}
	},
	created () {
	},
	mounted () {
		this.title = '測驗總覽'
		this.$set(this.selected, 'questions', this.selectedQuestions.map(n => (
			Object.keys(this.questions).find(i => this.questions[i][this.name] === n)
		)))
		this.$set(this.selected, 'rows', this.selectedRows)
	},
	methods: {
		async upload () {
			this.modified = true
			this.state = 'uploading'
			const formData = new FormData()
			formData.append('files', this.files.questions)
			formData.append('files', this.files.responses)
			const data = (await axios.post('/api/upload', formData)).data
			this.id = data.id
			this.questions = data.questions
			this.responses = data.responses
			this.$set(this.selected, 'questions', Object.keys(this.questions))
			this.$set(this.selected, 'rows', Object.keys(this.responses))
			this.state = 'finished'
		},
		linkQuestions () {
			this.selectedQuestions = Object.values(getCol(this.questions, this.selected.questions, this.name))
		},
		filter () {
			this.linkQuestions()
			const questions = {}
			Object.entries(loc(this.questions, this.selected.questions, [
				this.name, this.score, this.text, this.answer, this.type
			])).map((p, i) => {
				questions[i] = {
					name: p[1][this.name],
					score: p[1][this.score],
					text: p[1][this.text],
					answer: p[1][this.answer],
					type: (p[1][this.type] === this.boolean)
						? 'boolean'
						: (p[1][this.type] === this.discrete)
						? 'discrete'
						: (p[1][this.type] === this.continuous)
						? 'continuous'
						: 'others'
				}
			})
			this.testQuestions = questions
			this.testResponses = loc(this.responses, this.selectedRows, this.selectedQuestions)
		},
		analysis () {
			if (this.modified) {
				this.filter()
				this.action = null
			}
			this.$router.push({
        path: '/analysis'
      })
		}
	}
}
</script>

<style>

</style>
