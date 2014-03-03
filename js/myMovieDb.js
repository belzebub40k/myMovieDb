// render title cell
function renderTitle( data, type, row ) {
   return '<b id=' + row[5] + '>' + data + '</b>';}
   
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
      $('#movie_rating_votes').text(movie.rating_votes);
      $('#movie_studio').text(movie.studio);
      $('#movie_genre').text(movie.genre);
      $('#movie_runtime').text(movie.runtime);
      $('#movie_year').text(movie.year);
      $('#movie_country').text(movie.country);
      $('#movie_poster').attr('src', movie.thumbnails[0]);
      $('#movie_trailer').attr( 'src', 'https://www.youtube.com/embed/' + movie.youtube_id + '?wmode=transparent' );
      
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
   $('<table cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered" id="movies" data-cls="movies"></table>').appendTo( node );
   $('#movies').dataTable( {
      'aoColumns'  : [{'sTitle': 'TITLE',
                       'mRender': renderTitle,
                      },
                      {'sTitle': 'RATING', 'sWidth': '100px', 'bSearchable': false},
                      {'sTitle': 'YEAR','sWidth': '100px', 'bSearchable': false},
                      {'sTitle': 'GENRE', 'bSearchable': false},
                      {'sTitle': 'COUNTRY', 'bSearchable': false},
                     ],
      'bProcessing': true,
      'bPaginate': false,
      'sAjaxSource': 'data/movie_list.json',
      'sDom': '<"top">frt<"bottom"lp><"clear">'
   } );
   
   // apply bootstap styling
   $('#movies').each(function(){
      var datatable = $(this);
      // SEARCH - Add the placeholder for Search and Turn this into in-line form control
      var search_input = datatable.closest('.dataTables_wrapper').find('div[id$=_filter] input');
      search_input.attr('placeholder', 'Suche');
      search_input.addClass('form-control input-sm');
      // LENGTH - Inline-Form control
      var length_sel = datatable.closest('.dataTables_wrapper').find('div[id$=_length] select');
      length_sel.addClass('form-control input-sm');
   });
   
   // bind rowClick to all table-entries
   //$('#movies tbody').delegate("tr", "click", rowClick);
   $('#movies tbody').on("click", 'tr', rowClick);
   
   // stop videoplayback after modal-close
   $('#movie').on('hidden.bs.modal', function () {
      $('#movie_trailer').attr('src', '');
      $('#movie_poster').attr('src', '');
   });
   
   /*
   $('#movies').floatThead({
      useAbsolutePositioning: false
   });
   */
}
