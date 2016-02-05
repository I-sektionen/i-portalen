module.exports = function (grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        //This task puts all different js files into two big ones. (One for local use, one for production)
        concat: {
            options: { separator: ';'},
            dist: {
                src: 'wsgi/iportalen_django/**/js/src/*.js',  // Any .js files in a js/src folder is concat:ed
                dest: 'wsgi/iportalen_django/local_static/js/<%= pkg.name %>.js'
            }
        },

        //Waits for changes to files and then runs tasks.
        watch: {
            javascript_watch: {
                files: [
                'wsgi/iportalen_django/**/js/src/*.js',
                'wsgi/iportalen_django/**/.sass',
                'wsgi/iportalen_django/**/.scss'
                ],
                tasks: ['concat', 'copy', 'uglify', 'sass']
            }
        },

        sass: {
            dev: {
                options: {
                    style: 'expanded'
                },
                files: {
                    'wsgi/iportalen_django/local_static/css/<%= pkg.name %>.css':
                        'app.sass'
                }
            },
            dist: {
                options: {
                    style: 'compressed'
                },
                files: {
                    'wsgi/iportalen_django/iportalen/static/iportalen/css/<%= pkg.name %>.css':
                        'app.sass'
                }
            }
        },


        // Copies the concated js into a new folder. (This file is then minified)
        copy: {
            main: {
                files: {
                    'wsgi/iportalen_django/iportalen/static/iportalen/js/<%= pkg.name %>.js':
                        'wsgi/iportalen_django/local_static/js/<%= pkg.name %>.js'

                }
            }
        },

        //Minifies, mangles and removes comments & logging from *.min.js.
        uglify: {
            options: {
                compress: {
                    drop_console: true
                },
                screwIE8: true,
                preserveComments: false
            },
            my_target:{
                files: {
                    'wsgi/iportalen_django/iportalen/static/iportalen/js/<%= pkg.name %>.js':
                        'wsgi/iportalen_django/iportalen/static/iportalen/js/<%= pkg.name %>.js'
                }
            }
        }

    });
    /**
     * Load Grunt plugins dynamically
     */
    require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);
    grunt.registerTask('default', ['concat', 'copy', 'uglify', 'sass', 'watch']);
    };
