define(['jquery'], function () {
    function pytsiteGoogleMapsStaticMap(em) {
        var imgUrl = em.data('imgUrl');
        var link = em.data('link');
        var linkTarget = em.data('linkTarget');
        var width = parseInt(em.parent().width());
        var height = width;
        var img = $('<img src="' + imgUrl + '&size=' + width + 'x' + height + '">');

        em.find('a,img').remove();

        if (link !== undefined) {
            var a = $('<a href="' + link + '" target="' + linkTarget + '">');
            a.append(img);
            em.append(a);
        }
        else
            em.append(img);
    }

    return function (widget) {
        pytsiteGoogleMapsStaticMap(widget.em);
    };
});

