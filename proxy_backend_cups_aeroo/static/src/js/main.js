openerp.proxy_backend_cups_aeroo = function(instance) {

    var module = instance.proxy_backend;

	proxy_backend_cups_aeroo_device(instance,module);
    proxy_backend_cups_aeroo_print(instance,module);
    proxy_backend_cups_aeroo_widget(instance,module);
};
