// Run this before other modules
if (process.env.NEW_RELIC_LICENSE_KEY) {
  require('newrelic')
}

var compression = require('compression')
var cookieParser = require('cookie-parser')
var cookieSession = require('cookie-session')
var express = require('express')
var assets = require('connect-assets')
var browserify = require('browserify-middleware')
var babelify = require('babelify')
var bodyParser = require('body-parser')
var config = require('config')
var path = require('path')
var controllers = require('./app/controllers')
var resources = require('./app/resources')
var requestHandlers = require('./lib/request_handlers')
var middleware = require('./lib/middleware')
var logger = require('./lib/logger')()
var exec = require('child_process').exec

var app = module.exports = express()

app.locals.config = config

app.use(bodyParser.json())
app.use(compression())
app.use(cookieParser())
app.use(cookieSession({ secret: config.cookie_session_secret }))

app.use(requestHandlers.login_token_parser)
app.use(requestHandlers.request_log)
app.use(requestHandlers.request_id_echo)

app.set('view engine', 'jade')
app.set('views', __dirname + '/app/views')

// Redirect to environment-appropriate domain, if necessary
app.all('*', function (req, res, next) {
  if (config.header_host_port !== req.headers.host && app.locals.config.env !== 'development') {
    var redirectUrl = 'http://' + config.header_host_port + req.url
    console.log('req.hostname = %s but config.header_host_port = %s; redirecting to %s...', req.hostname, config.header_host_port, redirectUrl)
    res.redirect(301, redirectUrl)
  } else {
    next('route')
  }
})

app.get('/twitter-sign-in', controllers.twitter_sign_in.get)
app.get(config.twitter.oauth_callback_uri, controllers.twitter_sign_in_callback.get)

app.post('/api/v1/users', resources.v1.users.post)
app.get('/api/v1/users/:user_id', resources.v1.users.get)
app.put('/api/v1/users/:user_id', resources.v1.users.put)
app.delete('/api/v1/users/:user_id/login-token', resources.v1.users.delete)
app.get('/api/v1/users/:user_id/streets', resources.v1.users_streets.get)

app.post('/api/v1/streets', resources.v1.streets.post)
app.get('/api/v1/streets', resources.v1.streets.find)
app.head('/api/v1/streets', resources.v1.streets.find)

app.delete('/api/v1/streets/:street_id', resources.v1.streets.delete)
app.head('/api/v1/streets/:street_id', resources.v1.streets.get)
app.get('/api/v1/streets/:street_id', resources.v1.streets.get)
app.put('/api/v1/streets/:street_id', resources.v1.streets.put)

app.post('/api/v1/feedback', resources.v1.feedback.post)

app.get('/api/v1/translate/:locale_code/:resource_name', resources.v1.translate.get)

app.get('/.well-known/status', resources.well_known_status.get)

// Process stylesheets via Sass and PostCSS / Autoprefixer
app.use('/assets/css/styles.css', middleware.styles)

// Build JavaScript bundle via browserify
app.get('/assets/scripts/preinit.js', browserify(__dirname + '/assets/scripts/preinit.js', {
  cache: true,
  precompile: true,
  transform: [[{ presets: ['es2015'] }, babelify]]
}))
app.get('/assets/scripts/main.js', browserify(__dirname + '/assets/scripts/main.js', {
  cache: true,
  precompile: true,
  transform: [[{ presets: ['es2015'] }, babelify]],
  external: [__dirname + '/assets/scripts/preinit.js']
}))

// Build JavaScript bundle via concatenation
// Deprecated. Remove after scripts moved to browserify
app.use(assets({
  paths: ['assets/js'],
  precompile: ['app.js']
}))

// SVG bundled images served directly from packages
app.get('/assets/images/icons.svg', function (req, res) {
  res.sendFile(path.join(__dirname, '/node_modules/streetmix-icons/dist/icons.svg'))
})

app.get('/assets/images/images.svg', function (req, res) {
  res.sendFile(path.join(__dirname, '/node_modules/streetmix-illustrations/dist/images.svg'))
})

app.use(express.static(path.join(__dirname, '/public')))

// Catch-all
app.use(function (req, res) {
  res.render('main', {})
})

// Provide a message after a Ctrl-C
// Note: various sources tell us that this does not work on Windows
process.on('SIGINT', function () {
  if (app.locals.config.env === 'development') {
    console.log('Stopping Streetmix!')
    exec('npm stop')
  }
  process.exit()
})
