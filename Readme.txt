API接口测试项目，包含以下2个部分：
1.对单个接口的测试，即单个接口的功能，该接口和其他接口没有关联关系。
2.对有业务关联的接口的测试，即2个以上接口之间有依赖关系：
	涉及到测试数据的组织方式，有以下2种解决方案：
		(1)测试数据放在Excel文件中，其中请求参数部分(可能内容很长)放到yaml样本文件中，通过映射关系把Excel文件和yaml文件映射起来；
		(2)测试数据都放在Excel文件中。
	