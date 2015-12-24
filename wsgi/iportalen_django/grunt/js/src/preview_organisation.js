/**
 * Created by jonathan on 2015-12-18.
 */
//This function initiates the markdown engine. It is called on by event_preview below.
function markdown_organisation_preview() {
        var converter = Markdown.getSanitizingConverter();
        converter.hooks.chain("preConversion", function (text) {
            return text.replace(/[&<"'\/]/g, function (s) {
                var entityMap = {
                    "&": "&amp;",
                    "<": "&lt;",
                    '"': '&quot;',
                    "'": '&#39;',
                    "/": '&#x2F;'
                };
                return entityMap[s];
            }).replace(/([#]{2,})/g, '#').replace(/([=]{3,})/g, '').replace(/([-]{3,})/g, '').replace(/([`])/g, '');
        });
        converter.hooks.chain("plainLinkText", function (url) {
            return url.replace(/^https?:\/\//, "");
        });
        var editor = new Markdown.Editor(converter, "-body");
        editor.run();
    }
