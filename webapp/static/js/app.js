class UI {
  constructor(ui, client) {
    this._list = document.getElementById(ui.listId);
    this._button = document.querySelector(ui.buttonQuery);
    this._text = document.querySelector(ui.textQuery);

    this._before = ui.beforeClass;
    this._after = ui.afterClass;

    this._client = client
  }

  initialize() {
    this._list?.addEventListener('click', (event) => {
      if (event.target.tagName.toLowerCase() != 'button') { return; }

      event.preventDefault();
      this._button = event.target;
      this._text = event.target.querySelector('span');
      this._client.post(this._button.getAttribute('data-id'));
    });

    this._button?.addEventListener('click', (event) => {
      event.preventDefault();
      this._client.post(this._button.getAttribute('data-id'));
    });

    document.addEventListener('dataReady', (event) => {
      this._updateLikes(event.detail);
    });
  }

  _updateLikes(data) {
    if (data.error) { return; }

    this._text.textContent = data.likes;
    this._button.classList.replace(this._before, this._after);
  }
}

class Client {
  post(id) {
    fetch(this._request(id))
      .then((response) => response.json())
      .then((data) => this._emit(data))
  }

  _request(id) {
    return new Request('/tweets/likes', {
      method: 'POST',
      headers: {'X-CSRFToken': Cookies.get('csrftoken')},
      mode: 'same-origin', // Do not send CSRF token to another domain.
      body: JSON.stringify({ 'id': id })
    });
  }

  _emit(data) {
    document.dispatchEvent(
      new CustomEvent('dataReady', { detail: data })
    );
  }
}

(function() {
  window.addEventListener('load', () => {
    const ui = {
      listId: 'tweets-list',
      buttonQuery: '#single-tweet button',
      textQuery: '#single-tweet button span',
      beforeClass: 'tweet-footer__likes',
      afterClass: 'tweet-footer__liked'
    };
    (new UI(ui, new Client())).initialize();
  });
})();
