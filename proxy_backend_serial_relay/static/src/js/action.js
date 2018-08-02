function proxy_backend_serial_relay_action(instance, module){

    instance.web.client_actions.add("proxy_backend_serial_relay_on", "instance.proxy_backend_serial_relay.serial_relay_on");
    instance.proxy_backend_serial_relay.serial_relay_on = function (instance, context) {
        this.device_id = context.context.device_id;
        this.pin = context.context.pin;
        this.delay = context.context.delay;
        this.device_path = context.context.device_path;
        var parent = this;
        this.device = new openerp.proxy_backend.ProxyBackendDevice(
            this, this.device_id);
        this.device.get_device()
            .then(function(device){
                parent.backend_id = device.proxy_backend_id[0];
                parent.proxy = new openerp.proxy_backend.ProxyBackend(
                    this, parent.backend_id);
                return parent.proxy.get_backend();
            })
            .then(function(backend){
                if (backend != null){
                    parent.proxy.message_json(backend, "POST", "serial_relay_on", {"port": parent.device_path, "pin": parent.pin, "delay": parent.delay})
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

    instance.web.client_actions.add("proxy_backend_serial_relay_off", "instance.proxy_backend_serial_relay.serial_relay_off");
    instance.proxy_backend_serial_relay.serial_relay_off = function (instance, context) {
        this.device_id = context.context.device_id;
        this.pin = context.context.pin;
        this.delay = context.context.delay;
        this.device_path = context.context.device_path;
        
        var parent = this;
        this.device = new openerp.proxy_backend.ProxyBackendDevice(
            this, this.device_id);
        this.device.get_device()
            .then(function(device){
                parent.backend_id = device.proxy_backend_id[0];
                parent.proxy = new openerp.proxy_backend.ProxyBackend(
                    this, parent.backend_id);
                return parent.proxy.get_backend();
            })
            .then(function(backend){
                if (backend != null){
                    parent.proxy.message_json(backend, "POST", "serial_relay_off", {"port": parent.device_path, "pin": parent.pin, "delay": parent.delay})
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
