module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    less: {
      aabenthus: {
        files: {
          'stylesheets/aabenthus.css': 'less/aabenthus.less'
        }
      }
    },
    watch: {
      less: {
        files: [
          'less/**/*.less'
        ],
        tasks: ['less'],
      }
    },
    uglify: {
      javascript_libs: {
        options: {
          mangle: {
            except: ['jQuery']
          },
          sourceMap: true
        },
        files: {
          'javascripts/libs.min.js': [
            'bower_components/jquery/dist/jquery.js',
            'bower_components/bootstrap/dist/js/bootstrap.js',
            'bower_components/angular/angular.js',
            'bower_components/angular-ui-router/release/angular-ui-router.js',
            'bower_components/moment/moment.js',
            'bower_components/fullcalendar/dist/fullcalendar.js'
          ]
        }
      }
    },
    copy: {
      bootstrap: {
        expand: true,
        flatten: true,
        src: 'bower_components/bootstrap/fonts/*',
        dest: 'fonts/'
      }
    }
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy');

  // Default task(s).
  grunt.registerTask('default', ['less:aabenthus', 'copy:bootstrap', 'uglify:javascript_libs']);

};
