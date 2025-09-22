import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Progress } from './ui/progress';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { useToast } from '../hooks/use-toast';
import { Toaster } from './ui/toaster';
import LoadingSpinner, { SkeletonSection } from './LoadingSpinner';
import ErrorMessage, { ErrorSection } from './ErrorMessage';
import { portfolioApi } from '../services/api';
import { 
  Download, 
  Mail, 
  Phone, 
  MapPin, 
  Linkedin, 
  Menu, 
  X,
  Server,
  Shield,
  Network,
  Database,
  Monitor,
  FileText,
  ChevronDown,
  ChevronUp,
  Calendar,
  MapPinIcon,
  Languages,
  BookOpen,
  Code,
  Briefcase
} from 'lucide-react';

const Home = () => {
  // State management
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [expandedExperience, setExpandedExperience] = useState(null);
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [submitting, setSubmitting] = useState(false);
  const { toast } = useToast();

  // Data state
  const [personalInfo, setPersonalInfo] = useState(null);
  const [skills, setSkills] = useState([]);
  const [experience, setExperience] = useState([]);
  const [education, setEducation] = useState([]);
  const [languages, setLanguages] = useState([]);
  
  // Loading and error states
  const [loading, setLoading] = useState(true);
  const [errors, setErrors] = useState({});

  // Fetch all data on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [personalRes, skillsRes, expRes, eduRes, langRes] = await Promise.all([
          portfolioApi.getPersonalInfo().catch(err => ({ error: err })),
          portfolioApi.getSkills().catch(err => ({ error: err })),
          portfolioApi.getExperience().catch(err => ({ error: err })),
          portfolioApi.getEducation().catch(err => ({ error: err })),
          portfolioApi.getLanguages().catch(err => ({ error: err })),
        ]);
        
        // Handle responses and errors
        const newErrors = {};
        
        if (personalRes.error) {
          newErrors.personalInfo = personalRes.error;
        } else {
          setPersonalInfo(personalRes.data);
        }
        
        if (skillsRes.error) {
          newErrors.skills = skillsRes.error;
        } else {
          setSkills(skillsRes.data);
        }
        
        if (expRes.error) {
          newErrors.experience = expRes.error;
        } else {
          setExperience(expRes.data);
        }
        
        if (eduRes.error) {
          newErrors.education = eduRes.error;
        } else {
          setEducation(eduRes.data);
        }
        
        if (langRes.error) {
          newErrors.languages = langRes.error;
        } else {
          setLanguages(langRes.data);
        }
        
        setErrors(newErrors);
        
      } catch (error) {
        console.error('Error fetching data:', error);
        toast({
          title: "Error",
          description: "Failed to load portfolio data. Please refresh the page.",
          variant: "destructive"
        });
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [toast]);

  const retryFetch = (section) => {
    // Retry specific section
    const fetchSection = async () => {
      try {
        let response;
        switch (section) {
          case 'personalInfo':
            response = await portfolioApi.getPersonalInfo();
            setPersonalInfo(response.data);
            break;
          case 'skills':
            response = await portfolioApi.getSkills();
            setSkills(response.data);
            break;
          case 'experience':
            response = await portfolioApi.getExperience();
            setExperience(response.data);
            break;
          case 'education':
            response = await portfolioApi.getEducation();
            setEducation(response.data);
            break;
          case 'languages':
            response = await portfolioApi.getLanguages();
            setLanguages(response.data);
            break;
          default:
            return;
        }
        
        // Clear error for this section
        setErrors(prev => {
          const newErrors = { ...prev };
          delete newErrors[section];
          return newErrors;
        });
        
      } catch (error) {
        console.error(`Error retrying ${section}:`, error);
        toast({
          title: "Error",
          description: `Failed to reload ${section}. Please try again.`,
          variant: "destructive"
        });
      }
    };
    
    fetchSection();
  };

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setIsMenuOpen(false);
    }
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    
    try {
      await portfolioApi.submitContact(formData);
      toast({
        title: "Message Sent!",
        description: "Thank you for reaching out. I'll get back to you soon.",
      });
      setFormData({ name: '', email: '', message: '' });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to send message. Please try again.",
        variant: "destructive"
      });
    } finally {
      setSubmitting(false);
    }
  };

  const handleDownloadResume = () => {
    toast({
      title: "Resume Download",
      description: "Resume download will be available soon.",
    });
  };

  const skillIcons = {
    'Microsoft & Directory Services': Server,
    'Endpoint & Device Management': Monitor,
    'Networking & Security': Shield,
    'Backup & Recovery': Database,
    'RMM & Monitoring Tools': Network,
    'Ticketing & ITSM Tools': FileText
  };

  // Show loading state while data is being fetched
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800">
        {/* Header skeleton */}
        <header className="fixed top-0 w-full z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-700/50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="h-6 bg-slate-700 rounded w-32 animate-pulse"></div>
              <div className="hidden md:flex space-x-8">
                {Array.from({ length: 6 }).map((_, i) => (
                  <div key={i} className="h-4 bg-slate-700 rounded w-16 animate-pulse"></div>
                ))}
              </div>
            </div>
          </div>
        </header>
        
        {/* Hero skeleton */}
        <section className="min-h-screen flex items-center justify-center pt-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              <div className="text-center lg:text-left">
                <div className="h-16 bg-slate-700 rounded w-96 mx-auto lg:mx-0 mb-6 animate-pulse"></div>
                <div className="h-6 bg-slate-700 rounded w-80 mx-auto lg:mx-0 mb-4 animate-pulse"></div>
                <div className="h-4 bg-slate-700 rounded w-60 mx-auto lg:mx-0 mb-8 animate-pulse"></div>
                <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                  <div className="h-12 bg-slate-700 rounded w-40 animate-pulse"></div>
                  <div className="h-12 bg-slate-700 rounded w-32 animate-pulse"></div>
                </div>
              </div>
              <div className="flex justify-center">
                <div className="w-64 h-64 bg-slate-700 rounded-full animate-pulse"></div>
              </div>
            </div>
          </div>
        </section>
        
        <SkeletonSection title="About" cardCount={4} className="bg-slate-800/50" />
        <SkeletonSection title="Skills" cardCount={6} />
        <SkeletonSection title="Experience" cardCount={5} className="bg-slate-800/50" />
        <SkeletonSection title="Education" cardCount={2} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800">
      <Toaster />
      
      {/* Header */}
      <header className="fixed top-0 w-full z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="text-xl font-bold text-white">
              {personalInfo?.name || 'Loading...'}
            </div>
            
            {/* Desktop Navigation */}
            <nav className="hidden md:flex space-x-8">
              {['Home', 'About', 'Skills', 'Experience', 'Education', 'Contact'].map((item) => (
                <button
                  key={item}
                  onClick={() => scrollToSection(item.toLowerCase())}
                  className="text-slate-300 hover:text-white transition-colors duration-200 hover:-translate-y-0.5 transform"
                >
                  {item}
                </button>
              ))}
            </nav>

            {/* Mobile Menu Button */}
            <button
              className="md:hidden text-white"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>

          {/* Mobile Navigation */}
          {isMenuOpen && (
            <nav className="md:hidden py-4 border-t border-slate-700/50">
              {['Home', 'About', 'Skills', 'Experience', 'Education', 'Contact'].map((item) => (
                <button
                  key={item}
                  onClick={() => scrollToSection(item.toLowerCase())}
                  className="block w-full text-left py-2 text-slate-300 hover:text-white transition-colors"
                >
                  {item}
                </button>
              ))}
            </nav>
          )}
        </div>
      </header>

      {/* Hero Section */}
      <section id="home" className="min-h-screen flex items-center justify-center pt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="text-center lg:text-left">
              {errors.personalInfo ? (
                <ErrorMessage 
                  title="Unable to Load Profile"
                  message="Failed to load personal information."
                  onRetry={() => retryFetch('personalInfo')}
                />
              ) : (
                <>
                  <h1 className="text-5xl lg:text-7xl font-light text-white mb-6 leading-tight">
                    Hi, I'm <span className="text-blue-400 font-normal">
                      {personalInfo?.name?.split(' ')[0] || 'Loading...'}
                    </span>
                  </h1>
                  <p className="text-xl lg:text-2xl text-slate-300 mb-4">
                    {personalInfo?.role || 'Loading...'}
                  </p>
                  <p className="text-lg text-slate-400 mb-8">
                    {personalInfo?.sub_role || 'Loading...'}
                  </p>
                </>
              )}
              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <Button 
                  onClick={handleDownloadResume}
                  size="lg" 
                  className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg transition-all duration-200 hover:scale-105"
                >
                  <Download className="mr-2 h-4 w-4" />
                  Download Resume
                </Button>
                <Button 
                  onClick={() => scrollToSection('contact')}
                  variant="outline" 
                  size="lg"
                  className="border-slate-600 text-slate-300 hover:bg-slate-800 px-8 py-3 rounded-lg transition-all duration-200 hover:scale-105"
                >
                  <Mail className="mr-2 h-4 w-4" />
                  Contact Me
                </Button>
              </div>
            </div>
            
            <div className="flex justify-center">
              <div className="relative">
                <div className="absolute inset-0 rounded-full bg-gradient-to-r from-blue-400 to-purple-500 p-1 animate-pulse">
                  <div className="rounded-full bg-slate-900 p-4">
                    <Avatar className="w-64 h-64">
                      <AvatarImage src={personalInfo?.avatar} alt={personalInfo?.name} />
                      <AvatarFallback className="text-4xl bg-slate-800 text-white">
                        {personalInfo?.name?.split(' ').map(n => n[0]).join('') || 'SM'}
                      </AvatarFallback>
                    </Avatar>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 bg-slate-800/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-light text-white mb-4">About Me</h2>
            <div className="w-20 h-1 bg-blue-400 mx-auto"></div>
          </div>
          
          {errors.personalInfo ? (
            <ErrorMessage 
              title="Unable to Load About Information"
              message="Failed to load about section."
              onRetry={() => retryFetch('personalInfo')}
            />
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              <div>
                <p className="text-lg text-slate-300 leading-relaxed mb-8">
                  {personalInfo?.about_summary || 'Loading about information...'}
                </p>
                <div className="flex items-center gap-4 text-slate-400 mb-2">
                  <MapPin size={16} />
                  <span>{personalInfo?.location || 'Loading location...'}</span>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-6">
                <Card className="bg-slate-800/80 border-slate-700 hover:bg-slate-700/80 transition-all duration-200 hover:scale-105">
                  <CardContent className="pt-6 text-center">
                    <p className="text-white font-medium">7+ Years Experience</p>
                  </CardContent>
                </Card>
                <Card className="bg-slate-800/80 border-slate-700 hover:bg-slate-700/80 transition-all duration-200 hover:scale-105">
                  <CardContent className="pt-6 text-center">
                    <p className="text-white font-medium">Remote & Full-time Available</p>
                  </CardContent>
                </Card>
                <Card className="bg-slate-800/80 border-slate-700 hover:bg-slate-700/80 transition-all duration-200 hover:scale-105">
                  <CardContent className="pt-6 text-center">
                    <p className="text-white font-medium">Photography Enthusiast</p>
                  </CardContent>
                </Card>
                <Card className="bg-slate-800/80 border-slate-700 hover:bg-slate-700/80 transition-all duration-200 hover:scale-105">
                  <CardContent className="pt-6 text-center">
                    <p className="text-white font-medium">Continuous Learner</p>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Skills Section */}
      <section id="skills" className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-light text-white mb-4">Skills & Technologies</h2>
            <div className="w-20 h-1 bg-blue-400 mx-auto"></div>
          </div>
          
          {errors.skills ? (
            <ErrorMessage 
              title="Unable to Load Skills"
              message="Failed to load skills data."
              onRetry={() => retryFetch('skills')}
            />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {skills.map((skillGroup, index) => {
                const IconComponent = skillIcons[skillGroup.category] || Code;
                return (
                  <Card key={skillGroup.id || index} className="bg-slate-800/80 border-slate-700 hover:bg-slate-700/80 transition-all duration-300 hover:scale-105 group">
                    <CardHeader>
                      <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 bg-blue-600/20 rounded-lg group-hover:bg-blue-600/30 transition-colors">
                          <IconComponent className="h-5 w-5 text-blue-400" />
                        </div>
                        <CardTitle className="text-white text-lg">{skillGroup.category}</CardTitle>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="flex flex-wrap gap-2">
                        {skillGroup.items.map((skill, skillIndex) => (
                          <Badge key={skillIndex} variant="secondary" className="bg-slate-700 text-slate-300 hover:bg-slate-600">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          )}
        </div>
      </section>

      {/* Experience Section */}
      <section id="experience" className="py-20 bg-slate-800/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-light text-white mb-4">Experience</h2>
            <div className="w-20 h-1 bg-blue-400 mx-auto"></div>
          </div>
          
          {errors.experience ? (
            <ErrorMessage 
              title="Unable to Load Experience"
              message="Failed to load work experience data."
              onRetry={() => retryFetch('experience')}
            />
          ) : (
            <div className="space-y-6">
              {experience.map((exp, index) => (
                <Card key={exp.id || index} className="bg-slate-800/80 border-slate-700 hover:bg-slate-700/80 transition-all duration-200">
                  <CardHeader className="cursor-pointer" onClick={() => setExpandedExperience(expandedExperience === exp.id ? null : exp.id)}>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        {exp.logo && (
                          <img src={exp.logo} alt={exp.company} className="w-12 h-12 rounded-lg object-cover" />
                        )}
                        <div>
                          <CardTitle className="text-white text-xl">{exp.title}</CardTitle>
                          <CardDescription className="text-blue-400 text-lg">{exp.company}</CardDescription>
                          <div className="flex items-center gap-2 mt-1">
                            <Calendar size={14} className="text-slate-400" />
                            <span className="text-slate-400">{exp.duration}</span>
                          </div>
                        </div>
                      </div>
                      {expandedExperience === exp.id ? (
                        <ChevronUp className="text-slate-400" />
                      ) : (
                        <ChevronDown className="text-slate-400" />
                      )}
                    </div>
                  </CardHeader>
                  
                  {expandedExperience === exp.id && (
                    <CardContent className="pt-0">
                      <ul className="space-y-2">
                        {exp.highlights.map((highlight, highlightIndex) => (
                          <li key={highlightIndex} className="text-slate-300 flex items-start gap-2">
                            <div className="w-1.5 h-1.5 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
                            {highlight}
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  )}
                </Card>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Education Section */}
      <section id="education" className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-light text-white mb-4">Education</h2>
            <div className="w-20 h-1 bg-blue-400 mx-auto"></div>
          </div>
          
          {errors.education ? (
            <ErrorMessage 
              title="Unable to Load Education"
              message="Failed to load education data."
              onRetry={() => retryFetch('education')}
            />
          ) : (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {education.map((edu, index) => (
                  <Card key={edu.id || index} className="bg-slate-800/80 border-slate-700 hover:bg-slate-700/80 transition-all duration-200 hover:scale-105">
                    <CardHeader>
                      <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 bg-blue-600/20 rounded-lg">
                          <BookOpen className="h-5 w-5 text-blue-400" />
                        </div>
                        <div>
                          <CardTitle className="text-white">{edu.degree}</CardTitle>
                          <CardDescription className="text-blue-400">{edu.institution}</CardDescription>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Calendar size={14} className="text-slate-400" />
                        <span className="text-slate-400">{edu.year}</span>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="text-slate-300">{edu.description}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
              
              {/* Languages */}
              {errors.languages ? (
                <div className="mt-16">
                  <ErrorMessage 
                    title="Unable to Load Languages"
                    message="Failed to load language proficiency data."
                    onRetry={() => retryFetch('languages')}
                  />
                </div>
              ) : (
                <div className="mt-16">
                  <h3 className="text-2xl font-light text-white mb-8 text-center">Languages</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {languages.map((lang, index) => (
                      <div key={lang.id || index} className="text-center">
                        <div className="flex items-center gap-2 mb-2 justify-center">
                          <Languages size={16} className="text-blue-400" />
                          <span className="text-white font-medium">{lang.name}</span>
                        </div>
                        <Progress value={lang.level} className="h-2 bg-slate-700" />
                        <span className="text-slate-400 text-sm mt-1 block">{lang.level}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-20 bg-slate-800/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-light text-white mb-4">Get In Touch</h2>
            <div className="w-20 h-1 bg-blue-400 mx-auto"></div>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Contact Info */}
            <div className="space-y-8">
              <div>
                <h3 className="text-2xl font-light text-white mb-8">Contact Information</h3>
                {errors.personalInfo ? (
                  <ErrorMessage 
                    title="Unable to Load Contact Info"
                    message="Failed to load contact information."
                    onRetry={() => retryFetch('personalInfo')}
                  />
                ) : (
                  <div className="space-y-6">
                    <div className="flex items-center gap-4">
                      <div className="p-3 bg-blue-600/20 rounded-lg">
                        <Mail className="h-5 w-5 text-blue-400" />
                      </div>
                      <div>
                        <p className="text-slate-400">Email</p>
                        <p className="text-white">{personalInfo?.email || 'Loading...'}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-4">
                      <div className="p-3 bg-blue-600/20 rounded-lg">
                        <Phone className="h-5 w-5 text-blue-400" />
                      </div>
                      <div>
                        <p className="text-slate-400">Phone</p>
                        <p className="text-white">{personalInfo?.phone || 'Loading...'}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-4">
                      <div className="p-3 bg-blue-600/20 rounded-lg">
                        <MapPinIcon className="h-5 w-5 text-blue-400" />
                      </div>
                      <div>
                        <p className="text-slate-400">Location</p>
                        <p className="text-white">{personalInfo?.location || 'Loading...'}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-4">
                      <div className="p-3 bg-blue-600/20 rounded-lg">
                        <Linkedin className="h-5 w-5 text-blue-400" />
                      </div>
                      <div>
                        <p className="text-slate-400">LinkedIn</p>
                        <p className="text-white">{personalInfo?.linkedin || 'Loading...'}</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
            
            {/* Contact Form */}
            <div>
              <Card className="bg-slate-800/80 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white">Send Message</CardTitle>
                  <CardDescription className="text-slate-400">
                    Feel free to reach out for collaborations or just a friendly hello!
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleFormSubmit} className="space-y-6">
                    <div>
                      <Input
                        placeholder="Your Name"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-400"
                        required
                        disabled={submitting}
                      />
                    </div>
                    <div>
                      <Input
                        type="email"
                        placeholder="Your Email"
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-400"
                        required
                        disabled={submitting}
                      />
                    </div>
                    <div>
                      <Textarea
                        placeholder="Your Message"
                        value={formData.message}
                        onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                        className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-400 min-h-[120px]"
                        required
                        disabled={submitting}
                      />
                    </div>
                    <Button 
                      type="submit" 
                      className="w-full bg-blue-600 hover:bg-blue-700 text-white transition-all duration-200 hover:scale-105"
                      disabled={submitting}
                    >
                      {submitting ? (
                        <>
                          <LoadingSpinner size="sm" className="mr-2" />
                          Sending...
                        </>
                      ) : (
                        <>
                          <Mail className="mr-2 h-4 w-4" />
                          Send Message
                        </>
                      )}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-slate-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-slate-400 mb-4 md:mb-0">
              © 2025 {personalInfo?.name || 'Sarath M Warrier'}. All rights reserved.
            </div>
            <div className="flex space-x-6">
              <a href={`mailto:${personalInfo?.email}`} className="text-slate-400 hover:text-white transition-colors">
                <Mail size={20} />
              </a>
              <a href={`https://${personalInfo?.linkedin}`} target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-white transition-colors">
                <Linkedin size={20} />
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;