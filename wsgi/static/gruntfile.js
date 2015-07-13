module.exports = function (grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        sass: {
            dev: {
                options: {
                    style: "expanded"
                },
                files: {
                    'css/app.css': 'css/app.sass'
                }
            }
        },
        concat: {
            options: {
                separator: ';'
            },
            dist: {
                src: ['js/src/*.js'],
                dest: 'js/iportalen.js'
            }
        },
        jshint: {
            files: ['gruntfile.js', 'src/**/*.js'],
            options: {
                // options here to override JSHint defaults
                globals: {
                    jQuery: true,
                    console: true,
                    module: true,
                    document: true
                }
            }
        },
        watch: {
            sass: {
                files: ['css/**/*.sass', 'css/**/*.scss'],
                tasks: ['sass:dev']
            },
            concat: {
                files: ['js/src/**/*.js'],
                tasks: ['concat:dist']
            }
        }
    });
    /**
     * Load Grunt plugins dynaically
     */
    require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);
    grunt.registerTask('default', ['sass:dev', 'watch', 'concat']);
};