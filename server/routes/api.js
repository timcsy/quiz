const fs = require('fs').promises
fs.existsSync = require('fs').existsSync
const Router = require('koa-router')
const multer = require('@koa/multer')
const spawn = require('await-spawn')
const consola = require('consola')

const router = new Router()

router.prefix('/api')

const upload = multer()

function generateRandomString (length) {
  let text = ''
  const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  for (let i = 0; i < length; i++) { text += possible.charAt(Math.floor(Math.random() * possible.length)) }
  return text
}

async function saveFile (id, file) {
	if (!file) { return }
	const now = new Date()
	const formated = now.toISOString().replace(/[Z\-:]/g, '').replace(/[T.]/g, '_')
	const filename = formated + '_' + file.originalname
	const dirname = './static/tests/' + id + '/files'
	if (!fs.existsSync(dirname)) {
		await fs.mkdir(dirname, { recursive: true })
	}
	const f = await fs.open(dirname + '/' + filename, 'w+')
	await f.writeFile(file.buffer)
	await f.close()
	return dirname + '/' + filename
}

async function parse (path) {
	try {
		const program = await spawn('pipenv', ['run', 'python', 'server/bin/parse.py',
			path
		])
		consola.log(program.toString())
		return program.toString()
	} catch (err) {
		consola.error(err.stderr.toString())
		Promise.reject(err)
	}
}

async function analysis (id, test) {
	try {
		const program = await spawn('pipenv', ['run', 'python', 'server/bin/analysis.py',
			id, 'static/tests', JSON.stringify(test)
		])
		consola.log(program.toString())
		return program.toString()
	} catch (err) {
		consola.error(err.stderr.toString())
		Promise.reject(err)
	}
}

async function corr (id, columns) {
	try {
		const program = await spawn('pipenv', ['run', 'python', 'server/bin/corr.py',
			id, 'static/tests', JSON.stringify(columns)
		])
		consola.log(program.toString())
		return program.toString()
	} catch (err) {
		consola.error(err.stderr.toString())
		Promise.reject(err)
	}
}

async function split (id, first, second) {
	try {
		const program = await spawn('pipenv', ['run', 'python', 'server/bin/split.py',
			id, 'static/tests', JSON.stringify(first), JSON.stringify(second)
		])
		consola.log(program.toString())
		return program.toString()
	} catch (err) {
		consola.error(err.stderr.toString())
		Promise.reject(err)
	}
}

async function count (id, question) {
	try {
		const program = await spawn('pipenv', ['run', 'python', 'server/bin/count.py',
			id, 'static/tests', JSON.stringify(question)
		])
		consola.log(program.toString())
		return program.toString()
	} catch (err) {
		consola.error(err.stderr.toString())
		Promise.reject(err)
	}
}

router.post('/upload', upload.array('files'), async (ctx) => {
	const id = generateRandomString(20)
	const questionsPath = await saveFile(id, ctx.files[0])
	const responsesPath = await saveFile(id, ctx.files[1])
	let questions = {}
	let responses = {}
	if (questionsPath) { questions = JSON.parse(await parse(questionsPath)) }
	if (responsesPath) { responses = JSON.parse(await parse(responsesPath)) }
	ctx.body = { id, questions, responses }
})

router.post('/analysis', async (ctx) => {
	if (ctx.request.body.id) {
		ctx.body = await analysis(ctx.request.body.id, ctx.request.body.test)
	}
})

router.post('/corr', async (ctx) => {
	if (ctx.request.body.id) {
		ctx.body = await corr(ctx.request.body.id, ctx.request.body.columns)
	}
})

router.post('/split', async (ctx) => {
	if (ctx.request.body.id) {
		ctx.body = await split(ctx.request.body.id, ctx.request.body.first, ctx.request.body.second)
	}
})

router.get('/count', async (ctx) => {
	const question = {
		'name': 'A1',
		'type': 'discrete',
		'text': '1 + 1 = ?',
		'answer': 'A',
		'responses': [
			{ 'name': 'a', 'answer': 'B' },
			{ 'name': 'b', 'answer': 'A' },
			{ 'name': 'c', 'answer': 'A' }
		]
	}
	ctx.body = await count(ctx.request.body.id, question)
})

module.exports = router
