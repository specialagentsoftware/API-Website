$(document).ready(function () {
    // Initiate gifLoop for set interval
    var refresh;
    // Duration count in seconds
    const duration = 1000 * 10;
    // Giphy API defaults

    const giphysuccess = {
        baseURL: "https://api.giphy.com/v1/gifs/",
        apiKey: "0UTRbFtkMxAplrohufYco5IY74U8hOes",
        tag: "win",
        type: "random",
        rating: "R"
    };

    const giphyfail = {
        baseURL: "https://api.giphy.com/v1/gifs/",
        apiKey: "0UTRbFtkMxAplrohufYco5IY74U8hOes",
        tag: "fail",
        type: "random",
        rating: "R"
    };

    // Target gif-wrap container
    const $gif_wrap_success = $("#gif-wrap");
    const $gif_wrap_fail = $("#gif-wrap-fail");

    // Giphy API URL
    let giphyURL = encodeURI(
        giphysuccess.baseURL +
        giphysuccess.type +
        "?api_key=" +
        giphysuccess.apiKey +
        "&tag=" +
        giphysuccess.tag +
        "&rating=" +
        giphysuccess.rating
    );

    let giphyURLfail = encodeURI(
        giphyfail.baseURL +
        giphyfail.type +
        "?api_key=" +
        giphyfail.apiKey +
        "&tag=" +
        giphyfail.tag +
        "&rating=" +
        giphyfail.rating
    );


    // Display Gif in gif wrap container
    var renderGif = _giphy => {
        //console.log(_giphy);
        // Set gif as bg image
        $gif_wrap_success.css({
            "background-image": 'url("' + _giphy.image_original_url + '")'
        });
    };

    var renderGiffail = _giphyfail => {
        //console.log(_giphyfail);
        // Set gif as bg image
        $gif_wrap_fail.css({
            "background-image": 'url("' + _giphyfail.image_original_url + '")'
        })
    };

    if ($("#gif-wrap").length) {
        var newGif = () => $.getJSON(giphyURL, json => renderGif(json.data));
        newGif();
    } else {
        var newGiffail = () => $.getJSON(giphyURLfail, failjson => renderGiffail(failjson.data));
        newGiffail();
    }
}
);
