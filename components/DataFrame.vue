<template>
  <v-card>
		<v-simple-table v-if="simple">
			<template v-slot:default>
				<thead>
					<tr>
						<th />
						<th v-for="col in columns" :key="col" class="font-weight-black subtitle-2">
							{{ col }}
						</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="row in rows" :key="row.index">
						<td class="font-weight-black subtitle-2">
							{{ row.index }}
						</td>
						<td v-for="(item, i) in row.items" :key="i">
							{{ item }}
						</td>
					</tr>
				</tbody>
			</template>
		</v-simple-table>
		<v-data-table
			v-else
			v-bind="$attrs"
			v-on="$listeners"
			:headers="columns"
			:items="rows"
			:item-key="itemKey"
			v-model="value"
		>
			<template v-slot:item.$index="{ item }">
				<div class="font-weight-black subtitle-2">
					{{ item.$index }}
				</div>
			</template>
			<template v-for="(_, slot) of $scopedSlots" v-slot:[slot]="scope">
				<slot :name="slot" v-bind="scope" />
			</template>
		</v-data-table>
  </v-card>
</template>

<script>
export default {
	components: {
	},
	props: {
		data: {
			type: Object,
			default () {
        return {}
      }
		},
		simple: {
			type: Boolean,
			default: false
		},
		itemKey: {
			type: String,
			default: '$index'
		},
		selected: {
			type: Array,
			default () {
				return []
			}
		}
	},
	data () {
		return {
			value: []
		}
	},
	computed: {
		columns () {
			if (this.simple) {
				if (Object.keys(this.data).length > 0) {
					return Object.keys(Object.values(this.data)[0]).map(c => (c === null) ? 'nan' : c)
				} else {
					return {}
				}
			} else {
				if (this.$attrs.headers) { return this.$attrs.headers }
				if (Object.keys(this.data).length > 0) {
					const cols = Object.keys(Object.values(this.data)[0]).map(c => (c === null) ? 'nan' : c)
					return [ { value: '$index' }, ...cols.map(c => ({
						text: c,
						value: c,
						class: 'font-weight-black subtitle-2'
					})) ]
				} else {
					return [ { value: '$index' } ]
				}
			}
		},
		rows () {
			if (!this.simple && this.$attrs.items) { return this.$attrs.items }
			const table = []
			for (const i in this.data) {
				if (this.simple) {
					const row = { index: i, items: Object.values(this.data[i]).map(c => (c === null) ? 'nan' : c) }
					table.push(row)
				} else {
					const row = {}
					Object.entries(this.data[i]).forEach((pair) => {
						row[pair[0]] = (pair[1] === null) ? 'nan' : pair[1]
					})
					table.push({ '$index': i, ...row })
				}
			}
			return table
		}
	},
	watch: {
		value () {
			if (this.modified) {
				this.modified = false
			} else {
				this.$emit('update:selected', this.value.map(r => r[this.itemKey]))
			}
		},
		selected () {
			this.linkSelected()
		}
	},
	created () {
	},
	mounted () {
		this.linkSelected()
	},
	methods: {
		linkSelected () {
			let isEqual = true
			const selectedValues = []
			this.selected.forEach((i) => {
				const s = this.rows.find(v => v[this.itemKey] === i) // link to reference
				if (s !== undefined) { selectedValues.push(s) }
				if (!this.value.includes(s)) { isEqual = false }
			})
			this.value.forEach((v) => {
				if (!selectedValues.includes(v)) { isEqual = false }
			})
			if (!isEqual) {
				this.value = selectedValues
				this.modified = true
			}
		}
	}
}
</script>
