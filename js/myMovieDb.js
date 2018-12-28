// render title cell
function renderTitle( data, type, row ) {
   return '<b id=' + row[5] + '>' + data + '</b>';
}

/* render quality cell
function renderQuality( data, type, row ) {
   return '<img class="flags" src="media/lists/' + data + '.png"/>';
} */

// load movie information from file
function loadMovie(id) {
   $.getJSON('data/' + id + '.json', function(movie) {
      $('#movie_title').text(movie.title_local);
      $('#movie_plot').text(movie.plot);
      $('#movie_plot_outline').text(movie.plot_outline);
      $('#movie_title_original').text(movie.title_original);
      $('#movie_director').text(movie.director);
      $('#movie_writers').text(movie.writers);
      $('#movie_mpaa').text(movie.mpaa);
      $('#movie_rating').text(movie.rating);
      $('#movie_studio').text(movie.studio);
      $('#movie_genre').text(movie.genre);
      $('#movie_runtime').text(movie.runtime + ' min');
      $('#movie_premiere').text(movie.premiered);
      $('#movie_country').text(movie.country);
      $('#movie_poster').attr('src', movie.thumbnails[0]);
      $('#movie_trailer').attr( 'src', 'https://www.youtube.com/embed/' + movie.youtube_id + '?wmode=transparent' );
      $('#movie_flags').html('');

      $.each(movie.streams, function(idx,stream){
         if(stream.type == "v") {
            $('#movie_flags').append('<img class="flags" src="media/video/' + stream.resolution + '.png" />');
            $('#movie_flags').append('<img class="flags" src="media/video/' + stream.codec + '.png" />');
            if(stream.stereo != "") { $('#movie_flags').append('<img class="flags" src="media/video/3D.png" />'); }
         }
         if(stream.type == "a") {
            if ( $('#' + stream.codec).length == 0 ) {
               $('#movie_flags').append('<img id="' + stream.codec + '" class="flags" src="media/audio/' + stream.codec + '.png" />');
               $('#' + stream.codec).attr('data-original-title', stream.language +' '+ stream.channels);
               $('#' + stream.codec).attr('data-html', true);
               $('#' + stream.codec).tooltip()
            } else {
               var prev_title = $('#' + stream.codec).attr('data-original-title');
               $('#' + stream.codec).attr('data-original-title', prev_title +'<br/>'+ stream.language +' '+ stream.channels);
            }
         }
      });

      $('#movie').modal('toggle');
   });
}

// event-handler for row-click
function rowClick() {
   var id = $('td:first', this).find('b:first').attr('id');
   
   loadMovie(id)
}

function myMovieDb(node) {
   
   // add dynamic table
   // cellpadding="0" cellspacing="0" border="0"
   $('<table class="table table-striped table-bordered" id="movies" data-cls="movies"></table>').appendTo( node );
   $('#movies').dataTable( {
      'fixedHeader': true,
      'language'   : { 'search': '', 'searchPlaceholder': 'Search...' },
      'aoColumns'  : [{'sTitle': 'TITLE', 'mRender': renderTitle},
                      {'sTitle': 'GENRE'},
                      {'sTitle': 'RATING', 'sWidth': '50px', 'bSearchable': false},
                      {'sTitle': 'PREMIERE','sWidth': '100px', 'bSearchable': false},
                      {'sTitle': 'ADDED', 'sWidth': '100px', 'bSearchable': false},
                     ],
      'bProcessing': true,
      'bPaginate': false,
      'sAjaxSource': 'data/movie_list.json',
      'sDom': '<"top">frt<"bottom"lp><"clear">'
   } );

   // bind rowClick to all table-entries
   //$('#movies tbody').delegate("tr", "click", rowClick);
   $('#movies tbody').on("click", 'tr', rowClick);
   
   // stop videoplayback after modal-close
   $('#movie').on('hidden.bs.modal', function () {
      $('#movie_trailer').attr('src', '');
      $('#movie_poster').attr('src', '');
   });
}
