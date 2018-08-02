//TODO: Split into different file


openerp.proxy_backend = function(instance) {
    var QWeb = instance.web.qweb;
    instance.proxy_backend.ProxyBackend  = instance.web.Class.extend(openerp.PropertiesMixin,{
        init: function(parent, backend_id){
            this.backend_id = backend_id;
        },
        get_backend: function(){
            var obj_proxy = new openerp.Model("proxy.backend");
            return obj_proxy.query(["name","backend_ip", "port"])
                .filter([["id", "=", this.backend_id]])
                .first()
        },
        //TODO: find a way to eliminate backend parameter.
        message_json: function(backend, method, route, params){
            end_point = backend.backend_ip + ":" + backend.port + "/hw_proxy/" + route;
            return $.ajax(end_point, {
                type: method,
                contentType: "application/json",
                data: JSON.stringify({
                    "jsonrpc": "2.0",
                    "params": params
                }),
            });
        },
        message_http: function(backend, method, route, params){
            end_point = backend.backend_ip + ":" + backend.port + "/hw_proxy/" + route;
            return $.ajax(end_point, {
                type: method,
                contentType: "text/html",
            });
        },
    });

    instance.proxy_backend.ProxyBackendDevice  = instance.web.Class.extend(openerp.PropertiesMixin,{
        init: function(parent, device_id){
            this.device_id = device_id;
        },
        get_device: function(){
            var obj_device = new openerp.Model("proxy.backend_device");
            return obj_device.query(["name","proxy_backend_id"])
                .filter([["id", "=", this.device_id]])
                .first()
        },
    });

    //TODO: Check if there is any redundant method
    instance.proxy_backend.ProxyBackendWidget = instance.web.form.FormWidget.extend({
        className: "oe_form_widget_proxy_backend",
        init: function() {
            this._super.apply(this, arguments);
            this.options = instance.web.py_eval(this.node.attrs.options || "{}");
            this.proxy_backend_status = "disconnected";
        },
        start: function() {
            this._super();
            var parent = this;
            this.backend_id = this.field_manager.get_field_value(this.options.backend_id);
            this.proxy = new instance.proxy_backend.ProxyBackend(
                this, this.backend_id);
            this.display_info = this.options.display_info;
            this.set_connection("disconnected");

            this.update_connection();

            var weks = "field_changed:" + this.options.backend_id;
            this.field_manager.on(weks, this, function(){
                this.proxy.backend_id = this.field_manager.get_field_value(this.options.backend_id);
                this.update_connection();
            });
        },
        events: {
            "click .proxy_widget_test_button": "test_connection",
            "click .proxy_widget_configure_button": "configure_proxy_backend"
        },
        connect: function(event){
            var parent = this;
            this.proxy.get_backend()
                .then(function(backend){
                    parent.proxy.message_json(backend, "POST", "handshake", {})
                        .done(function(){
                            parent.set_connection("connected");
                        })
                        .fail(function(){
                            parent.set_connection("disconnected");
                        });
                })
        },
        test_connection: function(event){
            var parent = this;
            this.proxy.get_backend()
                .then(function(backend){
                    parent.proxy.message_json(backend, "POST", "handshake", {})
                        .done(function(){
                            alert("Connected to proxy backend");
                            parent.set_connection("connected");
                        })
                        .fail(function(){
                            alert("Failed to connect to proxy backend");
                            parent.set_connection("disconnected");
                        });
                })
        },
        update_connection: function(){
            console.log(this);
            if (this.backend_id != false){
                this.connect();
            }
            else {
                this.set_connection("disconnected");
            }
        },
        configure_proxy_backend: function(event){
            //TODO: Change into modal dialog
            //target == new makes it modal, but no mechanism to edit the form
            this.do_action({
                type: "ir.actions.act_window",
                res_model: "proxy.backend",
                res_id: this.backend_id,
                views: [[false, "form"]],
                target: "current",
                context: {},
            });
        },
        set_connection: function(data){
            this.proxy_backend_status = data;
            this.display_widget();
        },
        display_widget: function() {
            //Why this.renderElement() failed here?
            this.$el.html(QWeb.render("ProxyBackendWidget", {widget: this}));
        },
    });

    instance.web.form.custom_widgets.add("proxy_backend", "instance.proxy_backend.ProxyBackendWidget");

    instance.web.client_actions.add("test_proxy_backend_connection", "instance.proxy_backend.test_proxy_backend_connection");
    instance.proxy_backend.test_proxy_backend_connection = function (instance, context) {
        this.backend_id = context.context.backend_id;
        var parent = this;
        this.proxy = new openerp.proxy_backend.ProxyBackend(
            this, this.backend_id);
        this.proxy.get_backend()
            .then(function(backend){
                parent.proxy.message_json(backend, "POST", "handshake", {})
                    .done(function(){
                        alert("Connected to proxy backend");
                    })
                    .fail(function(){
                        alert("Failed to connect to proxy backend");
                    });
            })
    };

    instance.web.client_actions.add("test_proxy_device_connection", "instance.proxy_backend.test_proxy_device_connection");
    instance.proxy_backend.test_proxy_device_connection = function (instance, context) {
        this.device_id = context.context.device_id;
        var parent = this;
        this.device = new openerp.proxy_backend.ProxyBackendDevice(
            this, this.device_id);
        this.device.get_device()
            .then(function(device){
                parent.backend_id = device.proxy_backend_id[0];
                parent.device_name = device.name;
                parent.proxy = new openerp.proxy_backend.ProxyBackend(
                    this, parent.backend_id);
                return parent.proxy.get_backend();
            })
            .then(function(backend){
                if (backend != null){
                    parent.proxy.message_json(backend, "POST", "handshake", {})
                        .done(function(){
                            alert("Connected to proxy device");
                        })
                        .fail(function(){
                            alert("Failed to connect to proxy device");
                        });
                }
                //TODO: Find more elegant way
                else{
                    alert("Failed to connect to proxy device");
                }
            })
    };
}

