FROM rodolpheche/wiremock:2.27.2-alpine

COPY mappings /home/wiremock/mappings

CMD ["java", "-cp", "/var/wiremock/lib/*:/var/wiremock/extensions/*", "com.github.tomakehurst.wiremock.standalone.WireMockServerRunner","--global-response-templating"]