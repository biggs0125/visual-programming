/* eslint-disable */
var _ = require('lodash');
var fs = require('fs')
var gulp = require('gulp');
var babelify = require('babelify');
var source = require('vinyl-source-stream');
var browserify = require('browserify');
var watchify = require('watchify');
var gutil = require('gulp-util');
var path = require('path');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var through2 = require('through2');
var rename = require('gulp-rename');
var watch = require('gulp-watch');
var plumber = require('gulp-plumber');
var header = require('gulp-header');
var footer = require('gulp-footer');
var replace = require('gulp-replace');
var os = require('os');
//process.env.BROWSERIFYSWAP_DIAGNOSTICS = 1;
//process.env.BROWSERIFYSWAP_ENV = os.hostname().indexOf('bitly.org') !== -1 ? 'dev' : 'prod';

const CWD = process.cwd();
const ROOT = path.join(__dirname, '../app/');

const APP_JS_CONFIG = {
  src: './js/app.jsx',
  target: 'app.js',
  targetDir: '../static/js/'
}

const VENDOR_CONFIG = {
  src: [
    // why doesn't this work :(
    //'eventemitter3',
    'react',
    'react-mini-router',
    'react-highcharts',
    'immutable',
    'immstruct',
    'omniscient',
    'lodash',
    'bluebird',
    'moment'
  ],
  target: 'vendor.js',
  targetDir: '../static/js/'
};


const BROWSERIFY_OPTIONS = {
  debug: true,
  extensions: ['.js', '.jsx']
}


//
// Utility Functions
//
function bytesToKB(bytes) { return Math.floor(+bytes/1024); }

function logBundle(filename, watching) {
  return function (err, buf) {
    if (err) {
      return console.log(err.toString());
    }
    if (!watching) {
      gutil.log(filename + ' ' + bytesToKB(buf.length) + ' KB written');
    }
  }
}

function logWatch(filename) {
  return function(msg) {
    msg = msg.replace(/(\d+)\ bytes/, function(match, bytes) { return bytesToKB(bytes) + ' KB'; });
    gutil.log(filename + ' ' + msg);
  }
}

function logFileChange(filename) {
  gutil.log('change: ', filename.replace(ROOT, ''));
}

function bundleApp(b, config, watching) {
  return b.bundle(logBundle(config.target, watching))
    .pipe(source(config.target))
    .pipe(gulp.dest(config.targetDir));
}

function excludeVendor(b) {
  VENDOR_CONFIG.src.forEach(function(vendorLib) {
    b.exclude(vendorLib);
  });
}

var logVinylFile = through2.obj(function(file, enc, cb) {
  if (file != null) {
    var filename = path.basename(file.path);
    var filesize = file.contents ? bytesToKB(file.contents.length) : 0;
    gutil.log(filename + ' ' + filesize + ' KB written');

  }
  cb(null, file);
});

function buildJS(config) {
  var b = browserify(_.assign({entries: config.src}, BROWSERIFY_OPTIONS))
  .transform(babelify);

  excludeVendor(b);
  return bundleApp(b, config, false);
}

function watchJS(config) {
  watching = true;
  var w = watchify(browserify(_.assign({entries: config.src}, BROWSERIFY_OPTIONS, watchify.args)));
  var rebundle = function(files) {
    if (files != null && files.length) {
      files.forEach(function(file) {
        logFileChange(file);
      });
    }
    bundleApp(w, config, true);
  };

  w
  .transform(babelify);

  excludeVendor(w);
  w.on('update', rebundle);
  w.on('log', logWatch(config.target));
  rebundle();
}

gulp.task('vendor-build-js', function() {
  var b = browserify()
    .require(VENDOR_CONFIG.src);

  return b.bundle(logBundle(VENDOR_CONFIG.target))
    .pipe(source(VENDOR_CONFIG.target))
    .pipe(gulp.dest(VENDOR_CONFIG.targetDir));
});

gulp.task('app-build-js', function() { return buildJS(APP_JS_CONFIG); });

gulp.task('app-watch-js', function(cb) { watchJS(APP_JS_CONFIG); });

SASS_OPTIONS = {
  includePaths: ['./node_modules/susy/sass'],
  errLogToConsole: true
};

gulp.task('build-css', function() {
  gulp.src('./css/*.scss', {base: './css/'})
    .pipe(sourcemaps.init())
    .pipe(sass(SASS_OPTIONS))
    // @TODO get logVinylFile working again so we can see size of output file
    //.pipe(logVinylFile)
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('../static/css/'))
});

gulp.task('watch-css', ['build-css'], function(done) {
  watch('./css/**/*.scss', {
      base: './css/',
      read: false,
      verbose: true,
      // other events are too noisy and not needed
      events: ['change']
    }, function(file) {
      console.log(file);
      gulp.start('build-css');
    }
  )
});


gulp.task('dist', [
  'vendor-build-js',
  'app-build-js',
  'build-css'
]);

gulp.task('default', [
  'vendor-build-js',
  'app-watch-js',
  'watch-css'
]);


