
class Test:
	def __init__(self):
		pass;
	
	def run(self, test):
		pass;

class PIEmbedTest(Test):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.testName = "Lorem Ipsum is simply dummy text of the printing and typesetting industry.";
		self.testValue = """
		Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
		Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and 
		scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, 
		remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, 
		and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
		It is a long established fact that a reader will be distracted by the readable content ofapagewhenlookingatitslayout.ThepointofusingLoremIpsumisthatithasamore-or-lessnormaldistributionofletters, as opposed to using 'Content here, 
		content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as 
		their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have 
		evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
		Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, 
		making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more 
		obscureLatinwords,consectetur,fromaLoremIpsumpassage,andgoingthroughthecitesofthewordinclassicalliterature,discovered 
		theundoubtablesource.LoremIpsumcomesfromsections1.10.32and1.10.33of"deFinibusBonorumetMalorum"(The Extremes of Good and Evil) 
		by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, 
		"Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.
		The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" 
		by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.
		""";
		
	def execute(self):
		embed = PIEmbed(
			title="PIEmbed",
			description="Test."
		);
		embed.add.field(title=self.testName, content=self.testValue); # - TODO: Finish test -
