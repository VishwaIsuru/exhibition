from rotating_proxies.policy import BanDetectionPolicy


class MyBanPolicy(BanDetectionPolicy):
    def response_is_ban(self, request, response):
        # use default rules, but also consider HTTP 200 responses
        # a ban if there is 'captcha' word in response body.
        print('---iiiiiiiiiiiii-------------', response.url, response.status)
        ban = super(MyBanPolicy, self).response_is_ban(request, response)

        if 'hz' in response.url:
            print(response)
        if response.status == 404:
            ban = False

        if "we just need to make sure" in response.body:
            ban = True
        if response.status == 503:
            ban = True
        if "This website is using a security service to protect itself from online attacks." in response.body:
            ban = True
        if response.status == 503:
            ban = True
        return ban

    def exception_is_ban(self, request, exception):
        # override method completely: don't take exceptions in account
        return None
