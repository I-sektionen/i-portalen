module.exports = function (grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        sass: {
            dev: {
                options: {
                    style: "expanded"
                },
                files: {
                    'css/<%= pkg.name %>.css': 'css/app.sass'
                },
            },
            dist: {
                options: {
                    style: "compressed"
                },
                files: {
                    'dist/<%= pkg.name %>.min.css': 'css/app.sass'
                }
            },
        },
        concat: {
            options: {
                separator: ';'
            },
            dist: {
                src: ['js/src/*.js'],
                dest: 'js/<%= pkg.name %>.js'
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
        uglify: {
            dist: {
                src: ['<%= concat.dist.dest %>'],
                dest: 'dist/<%= pkg.name %>.min.js'
            },
            options: {
                banner: '/*! <%= pkg.name %> <%= grunt.template.today("dd-mm-yyyy") %> */\n'
            },

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
    grunt.registerTask('dist', ['sass:dist', 'uglify']);
};