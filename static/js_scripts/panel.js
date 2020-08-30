$(function() {
    var button_products = $('#button_products'),
    button_orders = $('#button_orders'),
    button_users = $('#button_users'),
    button_news = $('#button_news'),
    show_more_products = $('#show_more_products'),
    show_more_orders = $('#show_more_orders'),
    show_more_users = $('#show_more_users'),
    show_more_news = $('#show_more_news')
    ;

    var once_products = true;
    var once_orders = true;
    var once_users = true;
    var once_news = true;

    var skip_products = 0;
    const step_products = 5;
    var skip_orders = 0;
    const step_orders = 5;
    var skip_users = 0;
    const step_users = 5;
    var skip_news = 0;
    const step_news = 5;


    var table_products = $('#table_products'),
        table_orders = $('#table_orders'),
        table_users = $('#table_users'),
        table_news = $('#table_news');

    var tableProductsBody = $('<tbody>', {});
    table_products.border = '1'
    table_products.append(tableProductsBody);

    var tableOrdersBody = $('<tbody>', {});
    table_orders.border = '1'
    table_orders.append(tableOrdersBody);

    var tableUsersBody = $('<tbody>', {});
    table_users.border = '1'
    table_users.append(tableUsersBody);

    var tableNewsBody = $('<tbody>', {});
    table_news.border = '1'
    table_news.append(tableNewsBody);


    button_products.click(function(){
        $('#div_products').css("display", "block");
        $('#div_orders').css("display", "none");
        $('#div_users').css("display", "none");
        $('#div_news').css("display", "none");
        if(once_products){
            getDataProducts();
            once_products = false;
        }

    })
    show_more_products.click(getDataProducts)

    button_orders.click(function(){
        $('#div_products').css("display", "none");
        $('#div_orders').css("display", "block");
        $('#div_users').css("display", "none");
        $('#div_news').css("display", "none");
        if(once_orders){
            getDataOrders();
            once_orders = false;
        }
    })
    show_more_orders.click(getDataOrders)

    button_users.click(function(){
        $('#div_products').css("display", "none");
        $('#div_orders').css("display", "none");
        $('#div_users').css("display", "block");
        $('#div_news').css("display", "none");
        if(once_users){
            getDataUsers();
            once_users = false;
        }

    })
    show_more_users.click(getDataUsers)

    button_news.click(function(){
        $('#div_products').css("display", "none");
        $('#div_orders').css("display", "none");
        $('#div_users').css("display", "none");
        $('#div_news').css("display", "block");
        if(once_news){
            getDataNews();
            once_news = false;
        }

    })
    show_more_users.click(getDataUsers)


    function generateRowTable(/**/) {
        var args = arguments;
        var tr = $('<tr>', {
                    });


        for(var i=0; i<args.length; i++){
            var td = $('<td>', {
                    });
            td.text(args[i]);
            tr.append(td);
        }

        return tr;

    }




    function getDataProducts(){
        var send = {
            skip_products: skip_products,
            step_products: step_products
        };

        // make the selections disabled while fetching new data
        button_products.attr('disabled', true);
        button_orders.attr('disabled', true);
        button_users.attr('disabled', true);
        button_news.attr('disabled', true);

        $.post("/api/get_products", send, function(response, textStatus) {
            // we will need to add a handler for this in Flask
            console.log("Respuesta recibida de: /api/get_products", response);

            // populate
            // select_city.empty();
            $.each(response.products, function (index, value) {

                var tr = generateRowTable(
                    value.id_product, value.id_category,
                    value.name,
                    value.price
                );

                var td_stars = $('<td>', {

                          });

                for(var i=1; i<=parseInt(value.avgrating); i++){

                    td_stars.append(
                        $('<span>', {
                            class: 'fa fa-star checked text-warning'
                        })
                    )

                }

                for(var i=1; i<=(5-parseInt(value.avgrating)); i++){

                    td_stars.append(
                        $('<span>', {
                            class: 'fa fa-star'
                        })
                    )

                }

                tr.append(td_stars);
                var link_edit = $('<a>', {
                    href: "/admin/panel/updateProduct"
                          + "/" + value.id_product
                          + "/" + value.id_category
                          + "/" + value.name
                          + "/" + parseFloat(value.price)
                          + "/" + value.img_path.replaceAll("/", "_-SEP-_").replaceAll("\\", "_-SEP-_")
                            })

                link_edit.append($('<button>', {
                    class: 'btn btn-primary fa fa-edit'

                }))

                tr.append(link_edit);
                tableProductsBody.append(tr);




            });


        button_products.removeAttr('disabled');
        button_orders.removeAttr('disabled');
        button_users.removeAttr('disabled');
        button_news.removeAttr('disabled');

        if(response.products.length > 0)
            skip_products += step_products;
        else{
            alert('No more elements found');
        }

        }, "json");
    }

    function getDataOrders(){
        var send = {
            skip_orders: skip_orders,
            step_orders: step_orders
        };

        // make the selections disabled while fetching new data

        button_products.attr('disabled', true);
        button_orders.attr('disabled', true);
        button_users.attr('disabled', true);
        button_news.attr('disabled', true);

        $.post("/api/get_orders", send, function(response, textStatus) {
            // we will need to add a handler for this in Flask
            console.log("Respuesta recibida de: /api/get_orders", response);

            // populate
            // select_city.empty();
            $.each(response.orders_details, function (index, value) {


                tableOrdersBody.append(generateRowTable(
                    value.id_order, value.order_date,
                    value.username_user, value.product_name,
                    value.quantity, value.subtotal
                ));




            });



        button_products.removeAttr('disabled');
        button_orders.removeAttr('disabled');
        button_users.removeAttr('disabled');
        button_news.removeAttr('disabled');

        if(response.orders_details.length > 0)
            skip_orders += step_orders;

        else{
            alert('No more elements found');
        }

        }, "json");
    }

    function getDataUsers(){
        var send = {
            skip_users: skip_users,
            step_users: step_users
        };

        // make the selections disabled while fetching new data

        button_products.attr('disabled', true);
        button_orders.attr('disabled', true);
        button_users.attr('disabled', true);
        button_news.attr('disabled', true);

        $.post("/api/get_users", send, function(response, textStatus) {
            // we will need to add a handler for this in Flask
            console.log("Respuesta recibida de: /api/get_users", response);

            // populate
            // select_city.empty();
            $.each(response.users, function (index, value) {



                tableUsersBody.append(generateRowTable(
                    value.id, value.fullname,
                    value.email, value.username, value.country_name,
                    value.user_city
                ));




            });



        button_products.removeAttr('disabled');
        button_orders.removeAttr('disabled');
        button_users.removeAttr('disabled');
        button_news.removeAttr('disabled');

        if(response.users.length > 0)
            skip_users += step_users;
        else{
            alert('No more elements found');
        }

        }, "json");
    }

    function getDataNews(){
        var send = {
            skip_news: skip_news,
            step_news: step_news
        };

        // make the selections disabled while fetching new data
        button_products.attr('disabled', true);
        button_orders.attr('disabled', true);
        button_users.attr('disabled', true);
        button_news.attr('disabled', true);

        $.post("/api/get_news", send, function(response, textStatus) {
            // we will need to add a handler for this in Flask
            console.log("Respuesta recibida de: /api/get_news", response);

            // populate
            // select_city.empty();
            $.each(response.news, function (index, value) {


                var tr = generateRowTable(
                    value.id, value.author_user,
                    value.publish_date, value.title,
                    value.description, value.url,
                    value.id_news_category
                );


                tr.append($('<button>', {
                    class: 'btn btn-primary fa fa-edit'
                    onclick: function(){


                            $.post("/admin/panel/updateNew", value, function(response, textStatus) {
                                console.log("Respuesta recibida de: /admin/panel/updateNew", response);

                            })
                        }
                    }

                }))

                tableNewsBody.append(tr);




            });


        button_products.removeAttr('disabled');
        button_orders.removeAttr('disabled');
        button_users.removeAttr('disabled');
        button_news.removeAttr('disabled');

        if(response.news.length > 0)
            skip_news += step_news;
        else{
            alert('No more elements found');
        }

        }, "json");
    }


});
