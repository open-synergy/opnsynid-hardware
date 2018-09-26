function proxy_backend_cups_aeroo_widget(instance, module){
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.web.client_actions.add("get_cups_printer", "instance.proxy_backend_cups_aeroo.get_cups_printer");
    instance.proxy_backend_cups_aeroo.get_cups_printer = function (instance, context) {
        this.backend_id = context.context.backend_id;
        var parent = this;
        this.proxy = new openerp.proxy_backend.ProxyBackend(
            this, this.backend_id);
        var obj_proxy_cups_printer = new openerp.Model('proxy.cups_printer');
        this.proxy.get_backend()
            .then(function(backend){
                if (backend != null){
                    parent.proxy.message_json(backend, "POST", "get_printer_cups", {})
                        .done(function(printer){
                            obj_proxy_cups_printer.call('create_from_ui', [printer, backend]);
                        })
                        .fail(function(){
                            alert("Failed to connect to proxy device");
                        });
                }
                else{
                    alert("Failed to connect to proxy device");
                }
            })
    };
}

