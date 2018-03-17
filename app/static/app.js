/*
show delete button when focus on the input box
for both todolist and keepdolist
*/
$(".input-group .form-control").focus(function() {
  $('.input-group-btn#delete').hide();
  $(this).next().next().html("<i class='fas fa-minus-circle' id='delete-todo'></i>").show();
});

/*
call backend to delete the selected todo
handle both todo and keepdo
*/
$(".input-group-btn#delete").on('click', function() {
  var todo_id = $(this).parent().closest('div').attr('id').slice(4);
  console.log(todo_id);
  /*
  $.ajax({
    type: "POST",
    url: "/dashboard/drop-todo",
    dataType: "json",
    data: {
      todo_id: todo_id
    }
  });
  $(this).parent().closest('ul').html("").hide();
  */
});

/*
handle checkbox status and send it to the backend
*/
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

/*
click outside of the input box to update the todo content
*/
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

/*
check the status of whether todolist panels are collapsed or not
and send it to the backend
*/
$('#todolist-toggle').click(function(){
  // since the status of collapse will update after clicking
  // the logic here is reversed
  var todolist_collapse = $('#todolist-collapse').attr("class");
  if (todolist_collapse == "panel-collapse collapse in") {
    // panel is collapsed
    todolist_collapse = "";
  } else {
    // panel is expanded
    todolist_collapse = "in";
  }
  $.ajax({
    type: "POST",
    url: "/dashboard/session",
    dataType: "json",
    data: {
      todolist_collapse: todolist_collapse
    }
  })
});

/*
check the status of whether keepdolist panels are collapsed or not
and send it to the backend
*/
$('#keepdolist-toggle').click(function(){
  // since the status of collapse will update after clicking
  // the logic here is reversed
  var keepdolist_collapse = $('#keepdolist-collapse').attr("class");
  if (keepdolist_collapse == "panel-collapse collapse in") {
    // panel is collapsed
    keepdolist_collapse = "";
  } else {
    // panel is expanded
    keepdolist_collapse = "in";
  }
  $.ajax({
    type: "POST",
    url: "/dashboard/session",
    dataType: "json",
    data: {
      keepdolist_collapse: keepdolist_collapse
    }
  });
});

/*
daily check button
*/
$(".input-group-btn.daily-check").click(function() {
  var check_status = $(this).attr("id");
  $(this).attr("id", "check-checked");
  var keepdo_id = $(this).parent().attr("id").slice(6);
  if (check_status == "check-unchecked") {
    $.ajax({
      type: "POST",
      url: "/dashboard/checkin-keepdo",
      dataType: "json",
      data: {
        keepdo_id: keepdo_id
      },
      success: function(resp) {
        location.reload();
      }
    });
  } else {
    // for testing purpose
    $.ajax({
      type: "POST",
      url: "/dashboard/checkin-keepdo",
      dataType: "json",
      data: {
        keepdo_id: keepdo_id
      },
      success: function(resp) {
        location.reload();
      }
    });
  }
});
