function proxy_backend_solution_x100c_attendance_machine_action(instance, module){

    instance.web.client_actions.add("proxy_backend_solution_x100c_get_attendance", "instance.proxy_backend_solution_x100c_attendance_machine.get_attendance");
    instance.proxy_backend_solution_x100c_attendance_machine.get_attendance = function (instance, context) {
        this.device_id = context.context.device_id;
        this.ethernet_url = context.context.ethernet_url;
        this.key = context.context.ethernet_url;
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
                    parent.proxy.message_http(backend, "POST", "load_attendance_data")
                        .done(function(result){
                            var blob = new Blob([result], { type: 'text/csv;charset=utf-8;' });
                            var link = document.createElement("a");
                            var url = URL.createObjectURL(blob);
                            link.setAttribute("href", url);
                            link.setAttribute("download", "attendance.csv");
                            link.style.visibility = 'hidden';
                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                            console.log(blob);
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
