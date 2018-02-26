// show delete button when focus on input box
$(".input-group .form-control").focus(function() {
  $('.input-group-btn#delete').hide();
  $(this).next().next().html("<i class='fas fa-minus-circle' id='delete-todo'></i>").show();
});

// delete todo
$(".input-group-btn#delete").on('click', function() {
  var todo_id = $(this).parent().closest('div').attr('id').slice(4);
  $.ajax({
    type: "POST",
    url: "/dashboard/drop-todo",
    dataType: "json",
    data: {
      todo_id: todo_id
    }
  });
  $(this).parent().closest('ul').html("").hide();
});

// handle checkbox state and send it to backend
$('.todo-checkbox').click(function() {
  var todo_id = $(this).parent().closest('div').attr('id').slice(4);
  if (this.checked) {
    $(this).parent().next().css('text-decoration', 'line-through');
    $.ajax({
      type: "POST",
      url: "/dashboard/update-todo",
      dataType: "json",
      data: {
        todo_id: todo_id,
        task: "",
        status: "complete"
      }
    });
  } else {
    $(this).parent().next().css('text-decoration', 'none');
    $.ajax({
      type: "POST",
      url: "/dashboard/update-todo",
      dataType: "json",
      data: {
        todo_id: todo_id,
        task: "",
        status: "incomplete"
      }
    });
  }
});

// click outside of input box to update todo content
$(".input-group .form-control").on('input', function(){
  $('.input-group-btn#delete').hide();
}).on('change', function(){
  var todo_id = $(this).parent().closest('div').attr('id').slice(4);
  var task = $(this).val();
  $.ajax({
    type: "POST",
    url: "/dashboard/update-todo",
    dataType: "json",
    data: {
      todo_id: todo_id,
      task: task,
      status: ""
    }
  });
  $(this).next().html('<i class="far fa-check-circle"></i>&ensp;Saved').fadeIn('slow', function(){
    $(this).delay(1000).fadeOut('slow');
  });
});
