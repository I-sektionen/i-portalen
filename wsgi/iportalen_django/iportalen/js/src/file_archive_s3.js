/**
 * Created by jonathan on 2016-05-16.
 */
var s3exp_config = { Region: '', Bucket: '', Prefix: '', Delimiter: '/' };
var s3exp_lister = null;
var s3exp_columns = { key:1, date:2, size:3};
AWS.config.region = 'eu-central-1';
// Initialize S3 SDK and the moment library (for time formatting utilities)
var s3 = new AWS.S3();
moment().format();
function bytesToSize(bytes) {
    var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 Bytes';
    var ii = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return Math.round(bytes / Math.pow(1024, ii), 2) + ' ' + sizes[ii];
}
// Custom endsWith function for String prototype
if (typeof String.prototype.endsWith != 'function') {
    String.prototype.endsWith = function (str){
        return this.slice(-str.length) == str;
    };
}
function object2hrefvirt(bucket, object) {
    if (AWS.config.region === "us-east-1") {
        return document.location.protocol + '//' + bucket + '.s3.amazonaws.com/' + object;
    } else {
        return document.location.protocol + '//' + bucket + '.s3-' + AWS.config.region + '.amazonaws.com/' + object;
    }
}
function isthisdocument(bucket, object) {
    return object === "index.html";
}
function isfolder(path) {
    return path.endsWith('/');
}
// Convert cars/vw/golf.png to golf.png
function fullpath2filename(path) {
    return path.replace(/^.*[\\\/]/, '');
}
// Convert cars/vw/ to vw/
function prefix2folder(prefix) {
    var parts = prefix.split('/');
    return parts[parts.length-2] + '/';
}
// We are going to generate bucket/folder breadcrumbs. The resulting HTML will
// look something like this:
//
// <li>Home</li>
// <li>Library</li>
// <li class="active">Samples</li>
//
// Note: this code is a little complex right now so it would be good to find
// a simpler way to create the breadcrumbs.
function folder2breadcrumbs(data) {
    // The parts array will contain the bucket name followed by all the
    // segments of the prefix, exploded out as separate strings.
    var parts = [data.params.Bucket];
    if (data.params.Prefix) {
        parts.push.apply(parts,
                         data.params.Prefix.endsWith('/') ?
                         data.params.Prefix.slice(0, -1).split('/') :
                         data.params.Prefix.split('/'));
    }
    // Empty the current breadcrumb list
    $('#breadcrumb li').remove();
    // Now build the new breadcrumb list
    var buildprefix = '';
    $.each(parts, function(ii, part) {
        var ipart;
        // Add the bucket (the bucket is always first)
        if (ii === 0) {
            var a1 = $('<a>').attr('href', '#').text(part);
            ipart = $('<li>').append(a1);
            a1.click(function(e) {
                e.preventDefault();
                s3exp_config = {Bucket: data.params.Bucket, Prefix: '', Delimiter: data.params.Delimiter};
                (s3exp_lister = s3list(s3exp_config, s3draw)).go();
            });
        // Else add the folders within the bucket
        } else {
            buildprefix += part + '/';
            if (ii == parts.length - 1) {
                ipart = $('<li>').addClass('active').text(part);
            } else {
                var a2 = $('<a>').attr('href', '#').append(part);
                ipart = $('<li>').append(a2);
                // Closure needed to enclose the saved S3 prefix
                (function() {
                    var saveprefix = buildprefix;
                    a2.click(function(e) {
                        e.preventDefault();
                        s3exp_config = {Bucket: data.params.Bucket, Prefix: saveprefix, Delimiter: data.params.Delimiter};
                        (s3exp_lister = s3list(s3exp_config, s3draw)).go();
                    });
                })();
            }
        }
        $('#breadcrumb').append(ipart);
    });
}
function s3draw(data, complete) {
    $('li.li-bucket').remove();
    folder2breadcrumbs(data);
    // Add each part of current path (S3 bucket plus folder hierarchy) into the breadcrumbs
    $.each(data.CommonPrefixes, function(i, prefix) {
        $('#tb-s3objects').DataTable().rows.add([{Key: prefix.Prefix}]);
    });
    // Add S3 objects to DataTable
    $('#tb-s3objects').DataTable().rows.add(data.Contents).draw();
}
function s3list(config, completecb) {
    var params = { Bucket: config.Bucket, Prefix: config.Prefix, Delimiter: config.Delimiter };
    var scope = {
        Contents: [], CommonPrefixes:[], params: params, stop: false, completecb: completecb
    };
    return {
        // This is the callback that the S3 API makes when an S3 listObjects
        // request completes (successfully or in error). Note that a single call
        // to listObjects may not be enough to get all objects so we need to
        // check if the returned data is truncated and, if so, make additional
        // requests with a 'next marker' until we have all the objects.
        cb: function (err, data) {
            if (err) {
                scope.stop = true;
                alert("Error accessing S3 bucket " + scope.params.Bucket + ". Error: " + err);
            } else {
                // Store marker before filtering data
                if (data.IsTruncated) {
                    if (data.NextMarker) {
                        scope.params.Marker = data.NextMarker;
                    } else if (data.Contents.length > 0) {
                        scope.params.Marker = data.Contents[data.Contents.length - 1].Key;
                    }
                }
                // Filter the folders out of the listed S3 objects
                // (could probably be done more efficiently)
                data.Contents = data.Contents.filter(function(el) {
                    return el.Key !== scope.params.Prefix;
                });
                // Accumulate the S3 objects and common prefixes
                scope.Contents.push.apply(scope.Contents, data.Contents);
                scope.CommonPrefixes.push.apply(scope.CommonPrefixes, data.CommonPrefixes);
                // Update badge count to show number of objects read
                if (data.IsTruncated) {
                    s3.makeUnauthenticatedRequest('listObjects', scope.params, scope.cb);
                } else {
                    delete scope.params.Marker;
                    if (scope.completecb) {
                        scope.completecb(scope, true);
                    }
                }
            }
        },
        // Start the spinner, clear the table, make an S3 listObjects request
        go: function () {
            scope.cb = this.cb;
            $('#tb-s3objects').DataTable().clear();
            s3.makeUnauthenticatedRequest('listObjects', scope.params, this.cb);
        },
        stop: function () {
            scope.stop = true;
            delete scope.params.Marker;
            if (scope.completecb) {
                scope.completecb(scope, false);
            }
        }
    };
}
function resetDepth() {
    $('input[name="optionsdepth"]').val(['folder']);
    $('input[name="optionsdepth"][value="bucket"]').parent().removeClass('active');
    $('input[name="optionsdepth"][value="folder"]').parent().addClass('active');
}
function load_file_archive() {
    // Click handler for refresh button (to invoke manual refresh)
    $('#bucket-loader').click(function (e) {
        if ($('#bucket-loader').hasClass('fa-spin')) {
            // To do: We need to stop the S3 list that's going on
            // bootbox.alert("Stop is not yet supported.");
            s3exp_lister.stop();
        } else {
            delete s3exp_config.Marker;
            (s3exp_lister = s3list(s3exp_config, s3draw)).go();
        }
    });
    function renderObject(data, type, full) {
        if (isthisdocument(s3exp_config.Bucket, data)) {
            return fullpath2filename(data);
        } else if (isfolder(data)) {
            return '<a data-s3="folder" data-prefix="' + data + '" href="' + object2hrefvirt(s3exp_config.Bucket, data) + '">' + prefix2folder(data) + '</a>';
        } else {
            return '<a data-s3="object" href="' + object2hrefvirt(s3exp_config.Bucket, data) + '">' + fullpath2filename(data) + '</a>';
        }
    }

    // Initial DataTable settings
    $('#tb-s3objects').DataTable({
        iDisplayLength: 50,
        order: [[1, 'asc'], [0, 'asc']],
        aoColumnDefs: [
            { "aTargets": [ 0 ], "mData": "Key", "mRender": function (data, type, full) { return (type == 'display') ? renderObject(data, type, full) : data; }, "sType": "key" },
            { "aTargets": [ 1 ], "mData": "LastModified", "mRender": function (data, type, full) { return data ? moment(data).fromNow() : ""; } },
            { "aTargets": [ 2 ], "mData": function (source, type, val) { return source.Size ? ((type == 'display') ? bytesToSize(source.Size) : source.Size) : ""; } },
        ]
    });
    // Custom sort for the Key column so that folders appear before objects
    $.fn.dataTableExt.oSort['key-asc'] = function (a, b) {
        var x = (isfolder(a) ? "0-" + a : "1-" + a).toLowerCase();
        var y = (isfolder(b) ? "0-" + b : "1-" + b).toLowerCase();
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    };
    $.fn.dataTableExt.oSort['key-desc'] = function (a, b) {
        var x = (isfolder(a) ? "1-" + a : "0-" + a).toLowerCase();
        var y = (isfolder(b) ? "1-" + b : "0-" + b).toLowerCase();
        return ((x < y) ? 1 : ((x > y) ? -1 : 0));
    };

    // Delegated event handler for S3 object/folder clicks. This is delegated
    // because the object/folder rows are added dynamically and we do not want
    // to have to assign click handlers to each and every row.
    $('#tb-s3objects').on('click', 'a', function (event) {
        event.preventDefault();
        var target = event.target;
        // If the user has clicked on a folder then navigate into that folder
        if (target.dataset.s3 === "folder") {
            resetDepth();
            delete s3exp_config.Marker;
            s3exp_config.Prefix = target.dataset.prefix;
            s3exp_config.Delimiter = "/";
            (s3exp_lister = s3list(s3exp_config, s3draw)).go();
            // Else user has clicked on an object so download it in new window/tab
        } else {
            window.open(target.href, '_blank');
        }
        return false;
    });

    // Using technique from https://gist.github.com/jlong/2428561
    // to parse the document URL.
    var parser = document.createElement('a');
    parser.href = document.URL;
    // URL format is scheme://[user:password@]domain:port/path?query_string#fragment_id
    // For example: http://example.com:3000/path/?name=abc#topic

    // If initial bucket has been hard-coded above then use it, else try to
    // derive the initial bucket from the document URL (useful if index.html was
    // launched directly from within a bucket), else prompt the user.
    if (s3exp_config.Bucket) {
        (s3exp_lister = s3list(s3exp_config, s3draw)).go();
    } else if (parser.hostname.endsWith('amazonaws.com')) {
        // Hostname is likely to be in one of the following forms:
        // - s3.amazonaws.com
        // - bucket1.s3.amazonaws.com
        // - s3-us-west-2.amazonaws.com
        // - bucket2.s3-us-west-2.amazonaws.com
        var bucket;
        var region;
        var hostnames = parser.hostname.split('.');
        var pathnames = parser.pathname.split('/');
        // If bucket included in hostname
        if (hostnames.length == 4) {
            bucket = hostnames[0];
            region = hostnames[1];
        } else {
            bucket = pathnames[1];
            region = hostnames[0];
        }
        // If we found explicit region, for example s3-us-west-2, then use it
        // else use the default of US Standard
        if (region !== 's3') {
            AWS.config.region = region.substring(3);
        }
        // Create and initialize S3 object
        s3 = new AWS.S3();
        s3exp_config = { Bucket: bucket, Delimiter: '/' };
        // Do initial bucket list
        (s3exp_lister = s3list(s3exp_config, s3draw)).go();
    } else {
        resetDepth();
        s3exp_config = { Bucket: "iportalen-fillager", Delimiter: '/' };
        (s3exp_lister = s3list(s3exp_config, s3draw)).go();
    }
}