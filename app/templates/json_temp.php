{% extends "base.html" %}
  <!DOCTYPE html>
  <html style="padding-right: 15px; padding-left: 15px;">
  <head>
  <script src='https://code.jquery.com/jquery-1.12.3.js'></script>
  <script src='https://cdn.datatables.net/1.10.12/js/jquery.dataTables.min.js'></script>
  <script src="https://cdn.datatables.net/1.10.12/js/dataTables.bootstrap.min.js" charset="utf-8"></script>

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.12/css/dataTables.bootstrap.min.css">
      <link rel="stylesheet" href="https://cdn.datatables.net/responsive/2.1.0/css/responsive.bootstrap.min.css">
  


  <script>
    $(document).ready(function(){
$("#example").DataTable({
  // "sPaginationType": "bootstrap",
});
});
  </script>
  </head>
{% block content %}
<body>
<h1><span style='color:blue'>{{ name }}</span>, this is the <span style="color:chartreuse">JSON Export Page</span>.</h1>
<h4> </h4>
<h1>{{ user }}</h1>
<h2>Name: {{ name }} {{ lastname }}</h2>
{% if (page * 250) < total %}
    {% if (page - 1) <= 0 %}
      Page {{ page }}: Entries {{ ((page - 1) * 250) + 1 }} - {{ page * 250 }} out of {{ total }}.
    {% else %}
      Page {{ page }}: Entries {{ ((page - 1) * 250) }} - {{ page * 250 }} out of {{ total }}.
    {% endif %}
{% elif (page * 250) >= total %}
  Page {{ page }}: Entries {{ (page - 1) * 250 }} - {{ total }} out of {{ total }}.
{% endif %}
{% if (page - 3) <= 0 %}
    <nav aria-label="Page Nav" class="justify-content:center">
      <ul class="pagination" style="justify-content:center">
        <li class="page-item"><a class="page-link" href="/music_database_v2/1"><<</a></li>
    {% if (page - 1) <= 0 %}
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page }}"><-</a></li>
        {{ continue }}
    {% elif (page - 2) <= 0 %}
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-1 }}"><-</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-1 }}">{{ page-1 }}</a></li>
        {{ continue }}
    {% elif (page - 3) <= 0 %}
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-1 }}"><-</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-2 }}">{{ page-2 }}</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-1 }}">{{ page-1 }}</a></li>
        {{ continue }}
    {% else %}
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-1 }}"><-</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-1 }}">{{ page-3 }}</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-2 }}">{{ page-2 }}</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-3 }}">{{ page-1 }}</a></li>
    {% endif %}
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{page}}">{{ page }}</a></li>
        <li class="page-item"><a>...</a></li> 
        <a>
        <!-- Trigger the modal with a button -->
        <button type="button" class="btn btn-info btn-lg" data-toggle="modal" data-target="#myModal">Open Modal</button>

        <!-- Modal -->
        <div id="myModal" class="modal fade" role="dialog">
          <div class="modal-dialog">

            <!-- Modal content-->
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 class="modal-title">Modal Header</h4>
              </div>
              <div class="modal-body">
                <form method="POST" class="form-inline md-form mr-auto mb-4">
                  <input name="page_input" class="form-control mr-sm-2" type="text" placeholder="?" aria-label="Search">
                  <button class="btn aqua-gradient btn-rounded btn-sm my-0" type="submit">Search</button>
                </form>  
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
              </div>
            </div>
          </div>
        </div>
        </a>
        <li class="page-item"><a>...</a></li> 
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{page+1}}">{{ page+1 }}</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{page+2}}">{{ page+2 }}</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{page+3}}">{{ page+3 }}</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{page+1}}">-></a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{count}}">>></a></li>
{% elif (page + 3) >= count %}
    <nav aria-label="Page Nav" class="justify-content:center">
      <ul class="pagination" style="justify-content:center">
        <li class="page-item"><a class="page-link" href="/music_database_v2/1"><<</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-1 }}"><-</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-3 }}">{{ page-3 }}</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-2 }}">{{ page-2 }}</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-1 }}">{{ page-1 }}</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{page}}">{{ page }}</a></li>
        <li class="page-item"><a>...</a></li> 
        <a>
        <!-- Trigger the modal with a button -->
        <button type="button" class="btn btn-info btn-lg" data-toggle="modal" data-target="#myModal">Open Modal</button>

        <!-- Modal -->
        <div id="myModal" class="modal fade" role="dialog">
          <div class="modal-dialog">

            <!-- Modal content-->
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 class="modal-title">Modal Header</h4>
              </div>
              <div class="modal-body">
                <form method="POST" class="form-inline md-form mr-auto mb-4">
                  <input name="page_input" class="form-control mr-sm-2" type="text" placeholder="?" aria-label="Search">
                  <button class="btn aqua-gradient btn-rounded btn-sm my-0" type="submit">Search</button>
                </form>  
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
              </div>
            </div>
          </div>
        </div>
        </a>
        <li class="page-item"><a>...</a></li>
      {% if (page + 1) > count %}
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{page}}">-></a></li>
        {{ continue }}
      {% elif (page + 1) >= count %}
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{page+1}}">{{ page+1 }}</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{page+1}}">-></a></li>
        {{ continue }}
      {% elif (page + 2) >= count %}
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{page+1}}">{{ page+1 }}</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{page+2}}">{{ page+2 }}</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{page+2}}">-></a></li>
        {{ continue }}
      {% elif (page + 3) >= count %}
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page+1 }}">{{ page+1 }}</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page+2 }}">{{ page+2 }}</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page+3 }}">{{ page+3 }}</a></li>
        <li class="page-item"><a class="page-link" href="/music_database_v2/{{page+3}}">-></a></li>
        {{ continue }}
      {% endif %}
      <li class="page-item"><a class="page-link" href="/music_database_v2/{{count}}">>></a></li>
{% else %}
<nav aria-label="Page Nav" class="justify-content:center">
  <ul class="pagination" style="justify-content:center">
    <li class="page-item"><a class="page-link" href="/music_database_v2/1"><<</a></li>
    <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-1 }}"><-</a></li>
    <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-3 }}">{{ page-3 }}</a></li>
    <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-2 }}">{{ page-2 }}</a></li>
    <li class="page-item"><a class="page-link" href="/music_database_v2/{{ page-1 }}">{{ page-1 }}</a></li>
    <li class="page-item"><a class="page-link" href="/music_database_v2/{{page}}">{{ page }}</a></li>
    <li class="page-item"><a>...</a></li> 
    <a>
    <!-- Trigger the modal with a button -->
    <button type="button" class="btn btn-info btn-lg" data-toggle="modal" data-target="#myModal">Open Modal</button>

    <!-- Modal -->
    <div id="myModal" class="modal fade" role="dialog">
      <div class="modal-dialog">

        <!-- Modal content-->
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal">&times;</button>
            <h4 class="modal-title">Modal Header</h4>
          </div>
          <div class="modal-body">
            <form method="POST" class="form-inline md-form mr-auto mb-4">
              <input name="page_input" class="form-control mr-sm-2" type="text" placeholder="?" aria-label="Search">
              <button class="btn aqua-gradient btn-rounded btn-sm my-0" type="submit">Search</button>
            </form>  
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </a>
    <li class="page-item"><a>...</a></li>
    <li class="page-item"><a class="page-link" href="/music_database_v2/{{page+1}}">{{ page+1 }}</a></li>
    <li class="page-item"><a class="page-link" href="/music_database_v2/{{page+2}}">{{ page+2 }}</a></li>
    <li class="page-item"><a class="page-link" href="/music_database_v2/{{page+3}}">{{ page+3 }}</a></li>
    <li class="page-item"><a class="page-link" href="/music_database_v2/{{page+1}}">-></a></li>
    <li class="page-item"><a class="page-link" href="/music_database_v2/{{count}}">>></a></li>
{% endif %}
<form method="POST" class="form-inline md-form mr-auto mb-4">
  <input name= "search_bar" type="text" data-role="tagsinput">
  <button class="btn aqua-gradient btn-rounded btn-sm my-0" type="submit">Search</button>
</form>
<form method="POST" class="form-inline md-form mr-auto mb-4">
  <input name= "search_bar" type="text" class="form-control mr-sm-2" placeholder="Search">
  <button class="btn aqua-gradient btn-rounded btn-sm my-0" type="submit">Search</button>
</form>
<div class="table-responsive-lg">
  <table id="example" class="table table-striped table-bordered" cellspacing="0" width="100%">
    <thead>
        <tr>
        <th scope="col">#</th>
        <th scope="col">Cover Art</th>
        <th scope="col">Artist</th>
        <th scope="col">Title</th>
        <th scope="col">Album</th>
        <th scope="col">Length</th>
        <th scope="col">Genre</th>
        <th scope="col">Bitrate</th>
        <th scope="col">Preview</th>
        </tr>
    </thead>
    <tbody>
      {% for row in content %}
        <tr>
          <td>{{ row[0] }}</td>
          {% if row[8] == 1 %}
            {% set img_placeholder = "/cove/" + row[7] + " Cover Art.jpg" %}
          {% elif row[8] == 0 %}
            {% set img_placeholder = "/cove/ellsee.gif" %}
          {% endif %}
          <td><img style="max-width:40%; max-height:40%;" src="http://{{ ip + img_placeholder }}"></td>
          <td>{{ row[1] }}</td>
          <td>{{ row[2] }}</td>
          <td>{{ row[3] }}</td>
          <td>{{ row[4] }}</td>
          <td>{{ row[5] }}</td>
          <td>{{ row[6] }}</td>
          <td><audio class="playback" controls preload="none"><source src="http://{{ ip }}/muse/{{row[7]}}"></audio></td>
        </tr>
        {% endfor %}
    </tbody>
  </table>
</div>
</ul>
</nav>
{% endblock %}
</body>
<script>
$(document).ready(function () {
  $('#example').DataTable();
  "paging": True
});
$(function(){
    $("audio").on("play", function() {
        $("audio").not(this).each(function(index, audio) {
            audio.pause();
        });
    });
});
</script>
</html>