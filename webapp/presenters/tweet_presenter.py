class TweetPresenter:
    def __init__(self, tweet):
        self._tweet = tweet

    def id(self):
        return self._tweet.id

    def username(self):
        return self._tweet.user.username

    def display_name(self):
        return self._tweet.user.display_name

    def avatar_url(self):
        return self._tweet.user.avatar.url

    def message(self):
        return self._tweet.message

    def has_image(self):
        return bool(self._tweet.image)

    def image_url(self):
        return self._tweet.image.url

    def image_width(self):
        return self._tweet.image.width

    def image_height(self):
        return self._tweet.image.height

    def image_alt_text(self):
        pass

    def likes(self):
        return self._tweet.likes

    def button_class(self):
        if self._tweet.likes == 0:
            return 'tweet-footer__likes'
        return 'tweet-footer__liked'

    def created_at(self):
        return self._tweet.created_at
