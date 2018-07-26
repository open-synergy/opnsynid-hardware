function proxy_backend_gpio_action(instance, module){

    instance.web.client_actions.add('proxy_gpio_out_on', 'instance.proxy_backend_gpio.gpio_out_on');
    instance.proxy_backend_gpio.gpio_out_on = function (instance, context) {
        //PARAMETER
        this.device_id = context.context.device_id;
        this.channel = context.context.channel;
        this.mode = context.context.mode;
        //=========================================
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
                    parent.proxy.message_json(backend, "POST", "rpi_gpio_out_on", {"channel": parent.channel, "mode": parent.mode})
                        .done(function(){
                            // alert("Connected to proxy device");
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

    instance.web.client_actions.add('proxy_gpio_out_off', 'instance.proxy_backend_gpio.gpio_out_off');
    instance.proxy_backend_gpio.gpio_out_off = function (instance, context) {
        //PARAMETER
        this.device_id = context.context.device_id;
        this.channel = context.context.channel;
        this.mode = context.context.mode;
        //=========================================
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
                    parent.proxy.message_json(backend, "POST", "rpi_gpio_out_off", {"channel": parent.channel, "mode": parent.mode})
                        .done(function(){
                            // alert("Connected to proxy device");
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

    instance.web.client_actions.add('proxy_gpio_out_on_off_timer', 'instance.proxy_backend_gpio.gpio_out_on_off_timer');
    instance.proxy_backend_gpio.gpio_out_on_off_timer = function (instance, context) {
        //PARAMETER
        this.device_id = context.context.device_id;
        this.channel = context.context.channel;
        this.mode = context.context.mode;
        this.interval = context.context.interval;
        //=========================================
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
                    parent.proxy.message_json(backend, "POST", "rpi_gpio_out_on_off_timer", {"channel": parent.channel, "mode": parent.mode, "interval": parent.interval})
                        .done(function(){
                            // alert("Connected to proxy device");
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

};
