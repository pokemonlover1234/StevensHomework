#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

MODULE_INFO(vermagic, VERMAGIC_STRING);

__visible struct module __this_module
__attribute__((section(".gnu.linkonce.this_module"))) = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used
__attribute__((section("__versions"))) = {
	{ 0xdf6f06a4, __VMLINUX_SYMBOL_STR(module_layout) },
	{ 0x3d05a598, __VMLINUX_SYMBOL_STR(param_ops_int) },
	{ 0x29537c9e, __VMLINUX_SYMBOL_STR(alloc_chrdev_region) },
	{ 0x6091d207, __VMLINUX_SYMBOL_STR(cdev_add) },
	{ 0x3e5bd347, __VMLINUX_SYMBOL_STR(cdev_init) },
	{ 0xd8e484f0, __VMLINUX_SYMBOL_STR(register_chrdev_region) },
	{ 0x7485e15e, __VMLINUX_SYMBOL_STR(unregister_chrdev_region) },
	{ 0x367b8d99, __VMLINUX_SYMBOL_STR(cdev_del) },
	{ 0xdb7305a1, __VMLINUX_SYMBOL_STR(__stack_chk_fail) },
	{ 0xa1b6c2a6, __VMLINUX_SYMBOL_STR(mutex_unlock) },
	{ 0x706b7043, __VMLINUX_SYMBOL_STR(mutex_lock) },
	{ 0x56feef64, __VMLINUX_SYMBOL_STR(kmem_cache_alloc_trace) },
	{ 0xfff69224, __VMLINUX_SYMBOL_STR(kmalloc_caches) },
	{ 0x60b40fd8, __VMLINUX_SYMBOL_STR(copy_user_enhanced_fast_string) },
	{ 0xe5772d4a, __VMLINUX_SYMBOL_STR(copy_user_generic_string) },
	{ 0xdcc3a419, __VMLINUX_SYMBOL_STR(copy_user_generic_unrolled) },
	{ 0x1226bdb6, __VMLINUX_SYMBOL_STR(ex_handler_default) },
	{ 0xea4066e6, __VMLINUX_SYMBOL_STR(current_task) },
	{ 0x37a0cba, __VMLINUX_SYMBOL_STR(kfree) },
	{ 0x27e1a049, __VMLINUX_SYMBOL_STR(printk) },
	{ 0xbdfb6dbb, __VMLINUX_SYMBOL_STR(__fentry__) },
};

static const char __module_depends[]
__used
__attribute__((section(".modinfo"))) =
"depends=";

