ADMIN = """\
<!doctype html>
<html lang="en" class="h-100">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="Mark Otto, Jacob Thornton, Bootstrap contributors and Round Travel Team">
    <meta name="generator" content="Hugo 0.104.2">
    <title>Round Travel</title>
    <link href="https://round-travel.site/static/bootstrap.min.css" rel="stylesheet">

    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }

      .b-example-divider {
        height: 3rem;
        background-color: rgba(0, 0, 0, .1);
        border: solid rgba(0, 0, 0, .15);
        border-width: 1px 0;
        box-shadow: inset 0 .5em 1.5em rgba(0, 0, 0, .1), inset 0 .125em .5em rgba(0, 0, 0, .15);
      }

      .b-example-vr {
        flex-shrink: 0;
        width: 1.5rem;
        height: 100vh;
      }

      .bi {
        vertical-align: -.125em;
        fill: currentColor;
      }

      .nav-scroller {
        position: relative;
        z-index: 2;
        height: 2.75rem;
        overflow-y: hidden;
      }

      .nav-scroller .nav {
        display: flex;
        flex-wrap: nowrap;
        padding-bottom: 1rem;
        margin-top: -1px;
        overflow-x: auto;
        text-align: center;
        white-space: nowrap;
        -webkit-overflow-scrolling: touch;
      }
    </style>

    
    <!-- Custom styles for this template -->
    <link href="https://round-travel.site/static/cover.css" rel="stylesheet">
  </head>
  <body class="d-flex h-100 text-center text-bg-dark">
    
    <div class="cover-container d-flex w-100 h-100 p-3 mx-auto flex-column">
      <header class="mb-auto"></header>

      <main class="px-3">
        <h1>Добавить рекламщика</h1>
        <form action="https://round-travel.site/promo-admin/{{ secret }}" method="POST">
          <div class="mb-3">
            <input name="name" type="name" class="form-control" id="name_input">
          </div>
          <button type="submit" class="btn btn-primary">Добавить</button>
        </form></br></br>

        <h1>Рекламщики</h1>
        <table class="table table-dark table-striped">
        <thead>
          <tr>
            <th scope="col">Название</th>
          </tr>
        </thead>
        <tbody>
          {% for inviter in inviters %}
          <tr>
            <td>{{ inviter }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table></br></br>

        <h1>Реклама</h1>
        <table class="table table-dark table-striped">
        <thead>
          <tr>
            <th scope="col">Приглашающий</th>
            <th scope="col">Перешли по ссылке</th>
            <th scope="col">Загрузили</th>
          </tr>
        </thead>
        <tbody>
          {% for stat in inviter_stats %}
          <tr>
            <td>{{ stat[0] }}</td>
            <td>{{ stat[1] }}</td>
            <td>{{ stat[2] }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table></br></br>

      <h1>Клиенты</h1>
        <table class="table table-dark table-striped">
        <thead>
          <tr>
            <th scope="col">Имя</th>
            <th scope="col">Контакт</th>
            <th scope="col">От</th>
          </tr>
        </thead>
        <tbody>
          {% for client in clients %}
          <tr>
            <td>{{ client[0] }}</td>
            <td>{{ client[1] }}</td>
            <td>{{ client[2] }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
      </main>
      
      <footer class="mt-auto text-white-50"></footer>
    </div>
  </body>
</html>\
"""
