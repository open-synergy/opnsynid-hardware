function proxy_backend_cups_aeroo_device(instance, module){
    var QWeb = instance.web.qweb;
    _t = instance.web._t;

    var _super = module.ProxyBackendDevice;
    module.ProxyBackendDevice = module.ProxyBackendDevice.extend({
        print_using_cups: function(data){
            console.log(data)
            var self = this;
            if(data){
                this.receipt_queue.push(data);
            }
            var aborted = false;
            function send_printing_job(){
                if (self.receipt_queue.length > 0){
                    var r = self.receipt_queue.shift();
                    self.message('print_using_cups',{ data: r },{ timeout: 5000 })
                        .then(function(){
                            send_printing_job();
                        },function(error){
                            if (error) {
                                console.log("Error when printing")
                                return;
                            }
                            self.receipt_queue.unshift(r)
                        });
                }
            }
            send_printing_job();
        },
    });
};
