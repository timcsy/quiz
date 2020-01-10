<template>
  <v-app dark>
    <v-navigation-drawer
      v-model="drawer"
      fixed
      app
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      fixed
      app
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title v-text="title" />
      <v-spacer />
    </v-app-bar>
    <v-content>
      <v-container class="fill-height">
        <nuxt />
      </v-container>
    </v-content>
    <v-btn
      v-if="action"
      fab
      large
      dark
      fixed
      bottom
      right
    >
      <v-icon
        v-if="showTest"
        @click.stop="goTest()"
      >
        mdi-pencil
      </v-icon>
      <v-icon
        v-if="showAnalysis"
        @click.stop="goAnalysis()"
      >
        mdi-chart-bar
      </v-icon>
    </v-btn>
  </v-app>
</template>

<script>
import { mdiChartBar } from '@mdi/js'
import { mapFields } from 'vuex-map-fields'

export default {
	head () {
		return {
			title: this.$store.state.title,
			titleTemplate: '%s - Quiz'
		}
  },
  data () {
    return {
      drawer: false
    }
  },
  computed: {
    ...mapFields([
      'title',
      'action'
    ]),
    ...mapFields({
      items: 'drawer'
    }),
    showTest () {
      return this.action === 'test'
    },
    showAnalysis () {
      return this.action === 'analysis'
    }
  },
  methods: {
    goTest () {
      this.action = 'analysis'
      this.$router.push({
          path: '/test'
      })
    },
    goAnalysis () {
      this.$router.push({
          path: '/analysis'
      })
    }
  }
}
</script>
