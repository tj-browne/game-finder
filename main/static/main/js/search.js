const detailsUrlPattern = "/details/GAME_ID_PLACEHOLDER/";

$(document).ready(function () {
    $('.search-input').on('keydown', function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
        }
    });

    function debounce(func, delay) {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    }

    function performSearch(query) {
        $.ajax({
            type: 'GET',
            url: "/",
            data: {'query': query},
            dataType: 'json',
            success: function (response) {
                $('.card-container').empty();

                response.games.forEach(function (game) {
                    const detailUrl = detailsUrlPattern.replace('GAME_ID_PLACEHOLDER', game.id);
                    let gameCover = defaultImageUrl;
                    if (game.cover && game.cover.url) {
                        gameCover = game.cover.url;
                    }

                    const cardHtml = `
                        <div class="card">
                            <a class="card-link" href="javascript:void(0);" data-game-id="${game.id}" data-detail-url="${detailUrl}">
                                <img class="card-thumbnail" src="${gameCover}" alt="${game.name} cover">
                                <p class="card-title">${game.name}</p>
                            </a>
                        </div>
                    `;
                    $('.card-container').append(cardHtml);
                });

                $('.card-link').each(function () {
                    const detailUrl = $(this).data('detail-url');
                    $(this).on('click', function (event) {
                        event.preventDefault();
                        window.location.href = detailUrl;
                    });
                });

                $('html, body').animate({
                    scrollTop: $('.homepage-title').offset().top
                }, 700);
            },
            error: function (xhr, errmsg, err) {
                console.error(errmsg);
                $('.error-message').text('Error fetching games. Please try again later.').show();
            }
        });
    }

    $('.search-input').on('input', debounce(function (event) {
        event.preventDefault();
        const query = $(this).val().trim();
        if (query !== '') {
            performSearch(query);
        }
    }, 200));
});
