openerp.proxy_backend_gpio = function(instance) {

    var module = instance.proxy_backend;

	proxy_backend_gpio_device(instance,module);
    proxy_backend_gpio_action(instance,module);
};
