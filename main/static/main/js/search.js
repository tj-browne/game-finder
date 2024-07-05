$(document).ready(function () {
    $('.search-input').on('input', function (event) {
        event.preventDefault();
        const query = $(this).val().trim();

        if (query === '') {
            return;
        }

        $.ajax({
            type: 'GET',
            url: "/",  // Adjust the URL if necessary
            data: {'query': query},
            dataType: 'json',
            success: function (response) {
                $('.card-container').empty();

                response.games.forEach(function (game) {
                    // Construct the card HTML with data attributes for game details URL
                    const cardHtml = `
                        <div class="card">
                            <a class="card-link" href="javascript:void(0);" 
                               data-game-id="${game.id}" 
                               data-detail-url="{% url 'details' game_id=game.id %}">
                                <img class="card-thumbnail" 
                                     src="${game.cover.url || '{% static "main/images/imagenotfound.png" %}'}" 
                                     alt="${game.name} cover">
                                <p class="card-title">${game.name}</p>
                            </a>
                        </div>
                    `;
                    $('.card-container').append(cardHtml);
                });

                // Set up click event for dynamic card links
                $('.card-link').each(function () {
                    const detailUrl = $(this).data('detail-url');
                    $(this).on('click', function (event) {
                        event.preventDefault();
                        window.location.href = detailUrl;
                    });
                });
            },
            error: function (xhr, errmsg, err) {
                console.error(errmsg);
                $('.error-message').text('Error fetching games. Please try again later.').show();
            }
        });
    });
});