import $ from 'jquery';
import setupWidget from "@pytsite/widget";

setupWidget('plugins.google_maps_ui._widget.StaticMap', widget => {
    const imgUrl = widget.data('imgUrl');
    const link = widget.data('link');
    const linkTarget = widget.data('linkTarget');
    const width = parseInt(widget.em.parent().width());
    const height = width;
    const img = $('<img alt="Map" src="' + imgUrl + '&size=' + width + 'x' + height + '">');

    widget.find('a,img').remove();

    if (link !== undefined) {
        const a = $('<a href="' + link + '" target="' + linkTarget + '">');
        a.append(img);
        widget.em.append(a);
    } else {
        widget.em.append(img);
    }
});
