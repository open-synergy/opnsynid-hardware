function proxy_backend_gpio_device(instance, module){
    var QWeb = instance.web.qweb;
    _t = instance.web._t;

    var _super = module.ProxyBackendDevice;
    module.ProxyBackendDevice = module.ProxyBackendDevice.extend({
        rpi_gpio_out_on: function(channel, mode){
            this.message('rpi_gpio_out_on', {'channel' : channel, 'mode' : mode});
        },
        rpi_gpio_out_off: function(channel, mode){
            this.message('rpi_gpio_out_off', {'channel' : channel, 'mode' : mode});
        },
        rpi_gpio_out_on_off_timer: function(channel, mode, interval){
            this.message('rpi_gpio_out_on_off_timer', {'channel' : channel, 'mode' : mode, 'interval': interval});
        },
    });
};
