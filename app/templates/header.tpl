<!doctype html>

<html lang="en">

<head>
    <meta charset="utf-8">

    <title>{{title}}</title>
    <meta name="description" content="SSL certs status page for subdomain list">
    <link rel="stylesheet" href="static/styles.css?v=1.0">
    %if refresh:
    <script type="text/javascript">
        page_refresh = window.setTimeout(
            function () {
                window.location.href = window.location.href
            },
            {{ refresh }}* 2000);
    </script>

    <noscript>
        <meta http-equiv="refresh" content="{{refresh}}" />
    </noscript>
    %end
</head>

<body>
    <header>
    Running on: {{ hostname }} 
    | Redis available: {{ redis_available }}
    | Domains in Redis: {{ domains_in_redis }}
    | Domains in Web-App: {{ domains_in_webapp }}
    </header>