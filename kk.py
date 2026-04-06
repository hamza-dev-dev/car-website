import React, { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Users, UserPlus, Search, Trash2, GraduationCap, Briefcase, BookOpen } from "lucide-react";

const initialTeachers = [
  {
    id: 1,
    name: "الأستاذ أحمد بن يوسف",
    specialty: "الإعلام الآلي",
    level: "تقني سامي",
    phone: "0550 00 00 01",
    email: "ahmed@takwin.dz",
    experience: "12 سنة",
  },
  {
    id: 2,
    name: "الأستاذة سمية بوزيد",
    specialty: "المحاسبة",
    level: "تكوين مهني",
    phone: "0550 00 00 02",
    email: "somia@takwin.dz",
    experience: "9 سنوات",
  },
  {
    id: 3,
    name: "الأستاذ محمد قاسي",
    specialty: "الكهرباء الصناعية",
    level: "تقني",
    phone: "0550 00 00 03",
    email: "mohamed@takwin.dz",
    experience: "15 سنة",
  },
];

export default function TeachersListingWebsite() {
  const [teachers, setTeachers] = useState(initialTeachers);
  const [search, setSearch] = useState("");
  const [levelFilter, setLevelFilter] = useState("all");
  const [form, setForm] = useState({
    name: "",
    specialty: "",
    level: "تكوين مهني",
    phone: "",
    email: "",
    experience: "",
  });

  const levels = [...new Set(teachers.map((t) => t.level))];

  const filteredTeachers = useMemo(() => {
    return teachers.filter((teacher) => {
      const matchesSearch =
        teacher.name.includes(search) ||
        teacher.specialty.includes(search) ||
        teacher.level.includes(search) ||
        teacher.email.includes(search);
      const matchesLevel = levelFilter === "all" || teacher.level === levelFilter;
      return matchesSearch && matchesLevel;
    });
  }, [teachers, search, levelFilter]);

  const addTeacher = () => {
    if (!form.name || !form.specialty || !form.phone || !form.email || !form.experience) return;

    setTeachers((prev) => [
      {
        id: Date.now(),
        ...form,
      },
      ...prev,
    ]);

    setForm({
      name: "",
      specialty: "",
      level: "تكوين مهني",
      phone: "",
      email: "",
      experience: "",
    });
  };

  const deleteTeacher = (id) => {
    setTeachers((prev) => prev.filter((teacher) => teacher.id !== id));
  };

  return (
    <div className="min-h-screen bg-slate-50" dir="rtl">
      <div className="mx-auto max-w-7xl px-6 py-8">
        <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <Badge className="mb-3 rounded-full px-4 py-2">نظام إدارة الأساتذة</Badge>
              <h1 className="text-4xl font-bold text-slate-900">سيت إدراج الأساتذة في التكوين</h1>
              <p className="mt-2 text-slate-600">واجهة بسيطة وحديثة لإضافة الأساتذة، البحث عنهم، وتنظيم بياناتهم داخل مركز التكوين.</p>
            </div>
            <Card className="rounded-3xl shadow-sm">
              <CardContent className="flex items-center gap-4 p-6">
                <Users className="h-10 w-10" />
                <div>
                  <p className="text-sm text-slate-500">عدد الأساتذة</p>
                  <p className="text-3xl font-bold">{teachers.length}</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </motion.div>

        <div className="mb-8 grid gap-4 md:grid-cols-3">
          <Card className="rounded-3xl shadow-sm">
            <CardContent className="flex items-center gap-4 p-6">
              <GraduationCap className="h-9 w-9" />
              <div>
                <p className="text-sm text-slate-500">مستويات التكوين</p>
                <p className="text-2xl font-bold">{levels.length}</p>
              </div>
            </CardContent>
          </Card>
          <Card className="rounded-3xl shadow-sm">
            <CardContent className="flex items-center gap-4 p-6">
              <BookOpen className="h-9 w-9" />
              <div>
                <p className="text-sm text-slate-500">التخصصات المسجلة</p>
                <p className="text-2xl font-bold">{new Set(teachers.map((t) => t.specialty)).size}</p>
              </div>
            </CardContent>
          </Card>
          <Card className="rounded-3xl shadow-sm">
            <CardContent className="flex items-center gap-4 p-6">
              <Briefcase className="h-9 w-9" />
              <div>
                <p className="text-sm text-slate-500">الواجهة المناسبة للإدارة</p>
                <p className="text-2xl font-bold">جاهزة</p>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid gap-6 xl:grid-cols-3">
          <Card className="rounded-3xl shadow-sm xl:col-span-1">
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><UserPlus className="h-5 w-5" /> إضافة أستاذ جديد</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>الاسم الكامل</Label>
                <Input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} className="rounded-2xl" placeholder="أدخل اسم الأستاذ" />
              </div>

              <div className="space-y-2">
                <Label>التخصص</Label>
                <Input value={form.specialty} onChange={(e) => setForm({ ...form, specialty: e.target.value })} className="rounded-2xl" placeholder="مثال: إعلام آلي" />
              </div>

              <div className="space-y-2">
                <Label>المستوى</Label>
                <Select value={form.level} onValueChange={(value) => setForm({ ...form, level: value })}>
                  <SelectTrigger className="rounded-2xl">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="تكوين مهني">تكوين مهني</SelectItem>
                    <SelectItem value="تقني">تقني</SelectItem>
                    <SelectItem value="تقني سامي">تقني سامي</SelectItem>
                    <SelectItem value="مكون متخصص">مكون متخصص</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>رقم الهاتف</Label>
                <Input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} className="rounded-2xl" placeholder="0550 00 00 00" />
              </div>

              <div className="space-y-2">
                <Label>البريد الإلكتروني</Label>
                <Input value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} className="rounded-2xl" placeholder="name@takwin.dz" />
              </div>

              <div className="space-y-2">
                <Label>الخبرة</Label>
                <Input value={form.experience} onChange={(e) => setForm({ ...form, experience: e.target.value })} className="rounded-2xl" placeholder="مثال: 10 سنوات" />
              </div>

              <Button onClick={addTeacher} className="w-full rounded-2xl">حفظ الأستاذ</Button>
            </CardContent>
          </Card>

          <Card className="rounded-3xl shadow-sm xl:col-span-2">
            <CardHeader>
              <CardTitle>قائمة الأساتذة</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="mb-4 grid gap-3 md:grid-cols-2">
                <div className="relative">
                  <Search className="absolute right-3 top-3 h-4 w-4 text-slate-400" />
                  <Input
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="rounded-2xl pr-10"
                    placeholder="بحث بالاسم أو التخصص أو البريد"
                  />
                </div>
                <Select value={levelFilter} onValueChange={setLevelFilter}>
                  <SelectTrigger className="rounded-2xl">
                    <SelectValue placeholder="فلترة حسب المستوى" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">كل المستويات</SelectItem>
                    {levels.map((level) => (
                      <SelectItem key={level} value={level}>{level}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>الاسم</TableHead>
                      <TableHead>التخصص</TableHead>
                      <TableHead>المستوى</TableHead>
                      <TableHead>الهاتف</TableHead>
                      <TableHead>البريد</TableHead>
                      <TableHead>الخبرة</TableHead>
                      <TableHead></TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredTeachers.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={7} className="text-center text-slate-500">لا توجد نتائج مطابقة</TableCell>
                      </TableRow>
                    ) : (
                      filteredTeachers.map((teacher) => (
                        <TableRow key={teacher.id}>
                          <TableCell>{teacher.name}</TableCell>
                          <TableCell>{teacher.specialty}</TableCell>
                          <TableCell>{teacher.level}</TableCell>
                          <TableCell>{teacher.phone}</TableCell>
                          <TableCell>{teacher.email}</TableCell>
                          <TableCell>{teacher.experience}</TableCell>
                          <TableCell>
                            <Button variant="ghost" size="icon" onClick={() => deleteTeacher(teacher.id)}>
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
